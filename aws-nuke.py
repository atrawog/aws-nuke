#!/usr/bin/env python

import boto3
import click
import os
import botocore

# Ensure you have set the following environment variables:
# AWS_ACCESS_KEY_ID: Your AWS Access Key ID
# AWS_SECRET_ACCESS_KEY: Your AWS Secret Access Key
# AWS_DEFAULT_REGION: The AWS region you want to interact with

def perform_deletion(resource_name, list_func, delete_func, dry_run):
    resources = list_func()
    for resource in resources:
        resource_id = resource['id']
        if dry_run:
            print(f'Dryrun deleting {resource_name}: {resource_id}')
        else:
            print(f'Deleting {resource_name}: {resource_id}')
            delete_func(resource, dry_run)

def list_s3_buckets():
    s3 = boto3.resource('s3')
    return [{'id': bucket.name, 'object': bucket} for bucket in s3.buckets.all()]

def delete_s3_bucket(bucket, dry_run):
    if dry_run:
        print(f"Dry run: Would delete S3 bucket {bucket['id']}")
    else:
        bucket['object'].objects.all().delete()
        bucket['object'].delete()
        print(f"Deleted S3 bucket {bucket['id']}")

def list_ec2_instances():
    ec2 = boto3.resource('ec2')
    return [{'id': instance.id, 'object': instance} for instance in ec2.instances.all()]

def delete_ec2_instance(instance, dry_run):
    if dry_run:
        print(f"Dry run: Would terminate EC2 instance {instance['id']}")
    else:
        instance['object'].terminate()
        print(f"Terminated EC2 instance {instance['id']}")

def list_iam_roles():
    iam = boto3.client('iam')
    return [{'id': role['RoleName']} for role in iam.list_roles()['Roles']]

def delete_iam_role(role, dry_run):
    iam = boto3.client('iam')

    # Skip protected service-linked roles
    if role['id'].startswith('AWSServiceRoleFor'):
        print(f"Skipping deletion of service-linked role: {role['id']}")
        return

    # List instance profiles associated with the role
    instance_profiles = iam.list_instance_profiles_for_role(RoleName=role['id'])['InstanceProfiles']
    
    if dry_run:
        for profile in instance_profiles:
            print(f"Dry run: Would remove role {role['id']} from instance profile {profile['InstanceProfileName']}")
    else:
        # Remove the role from instance profiles
        for profile in instance_profiles:
            iam.remove_role_from_instance_profile(InstanceProfileName=profile['InstanceProfileName'], RoleName=role['id'])
            print(f"Removed role {role['id']} from instance profile {profile['InstanceProfileName']}")

    # Detach managed policies
    attached_policies = iam.list_attached_role_policies(RoleName=role['id'])['AttachedPolicies']
    
    if dry_run:
        for policy in attached_policies:
            print(f"Dry run: Would detach managed policy {policy['PolicyArn']} from role {role['id']}")
    else:
        for policy in attached_policies:
            iam.detach_role_policy(RoleName=role['id'], PolicyArn=policy['PolicyArn'])
            print(f"Detached managed policy {policy['PolicyArn']} from role {role['id']}")

    # Delete inline policies
    inline_policies = iam.list_role_policies(RoleName=role['id'])['PolicyNames']
    
    if dry_run:
        for policy_name in inline_policies:
            print(f"Dry run: Would delete inline policy {policy_name} from role {role['id']}")
    else:
        for policy_name in inline_policies:
            iam.delete_role_policy(RoleName=role['id'], PolicyName=policy_name)
            print(f"Deleted inline policy {policy_name} from role {role['id']}")

    # Now delete the role
    if dry_run:
        print(f"Dry run: Would delete IAM role {role['id']}")
    else:
        iam.delete_role(RoleName=role['id'])
        print(f"Deleted IAM role: {role['id']}")

def list_kms_keys():
    kms = boto3.client('kms')
    return [{'id': key['KeyId']} for key in kms.list_keys()['Keys']]

def delete_kms_key(key, dry_run):
    kms = boto3.client('kms')
    
    if dry_run:
        print(f"Dry run: Would schedule deletion for KMS key {key['id']}")
    else:
        try:
            kms.schedule_key_deletion(KeyId=key['id'], PendingWindowInDays=7)
            print(f"Scheduled deletion for KMS key {key['id']}")
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                print(f"Warning: Access denied for scheduling deletion of KMS key {key['id']}. Please check your permissions.")
            else:
                print(f"Warning: Failed to schedule deletion for KMS key {key['id']} due to error: {e}")


# Add similar functions for other AWS resources...

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-f', '--force', is_flag=True, help='Perform actual deletions.')
@click.option('-a', '--all', is_flag=True, help='Delete all resources.')
@click.option('--s3-buckets', is_flag=True, help='Delete S3 buckets.')
@click.option('--ec2-instances', is_flag=True, help='Delete EC2 instances.')
@click.option('--iam-roles', is_flag=True, help='Delete IAM roles.')
@click.option('--kms-keys', is_flag=True, help='Delete KMS keys.')
@click.pass_context
def main(ctx, force, all, s3_buckets, ec2_instances, iam_roles, kms_keys):
    
    # Default to dry run unless --force is specified
    dry_run = not force

    # Show help if no options are provided
    if not any([force, all, s3_buckets, ec2_instances, iam_roles, kms_keys]):
        click.echo(ctx.get_help())
        ctx.exit()

    # If --all is specified, set all resource options to True
    if all:
        s3_buckets = ec2_instances = iam_roles = kms_keys = True

    if s3_buckets:
        perform_deletion("S3 bucket", list_s3_buckets, delete_s3_bucket, dry_run)
    
    if ec2_instances:
        perform_deletion("EC2 instance", list_ec2_instances, delete_ec2_instance, dry_run)
    
    if iam_roles:
        perform_deletion("IAM role", list_iam_roles, delete_iam_role, dry_run)
    
    if kms_keys:
        perform_deletion("KMS key", list_kms_keys, delete_kms_key, dry_run)

if __name__ == "__main__":
    # Ensure environment variables are set before running the script
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        raise EnvironmentError("AWS credentials are not set in environment variables.")
    
    main()
