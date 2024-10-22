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
            print(f'Dry run: Would delete {resource_name}: {resource_id}')
        else:
            print(f'Deleting {resource_name}: {resource_id}')
            delete_func(resource, dry_run)

# Function to list and delete CloudWatch logs
def list_cloudwatch_logs():
    logs = boto3.client('logs')
    log_groups = logs.describe_log_groups()['logGroups']
    return [{'id': log_group['logGroupName']} for log_group in log_groups]

def delete_cloudwatch_log(log, dry_run):
    logs = boto3.client('logs')
    if dry_run:
        print(f"Dry run: Would delete CloudWatch log group {log['id']}")
    else:
        logs.delete_log_group(logGroupName=log['id'])
        print(f"Deleted CloudWatch log group {log['id']}")

# Function to list and delete KMS keys
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

# Function to list and delete RDS instances
def list_rds_instances():
    rds = boto3.client('rds')
    return [{'id': instance['DBInstanceIdentifier']} for instance in rds.describe_db_instances()['DBInstances']]

def delete_rds_instance(instance, dry_run):
    rds = boto3.client('rds')
    if dry_run:
        print(f"Dry run: Would delete RDS instance {instance['id']}")
    else:
        try:
            rds.delete_db_instance(DBInstanceIdentifier=instance['id'], SkipFinalSnapshot=True)
            print(f"Deleted RDS instance {instance['id']}")
        except botocore.exceptions.ClientError as e:
            print(f"Warning: Failed to delete RDS instance {instance['id']} due to error: {e}")

# Example functions for other AWS services (already present)
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

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-f', '--force', is_flag=True, help='Perform actual deletions.')
@click.option('-a', '--all', is_flag=True, help='Delete all resources.')
@click.option('--s3-buckets', is_flag=True, help='Delete S3 buckets.')
@click.option('--ec2-instances', is_flag=True, help='Delete EC2 instances.')
@click.option('--cloudwatch-logs', is_flag=True, help='Delete CloudWatch log groups.')
@click.option('--kms-keys', is_flag=True, help='Delete KMS keys.')
@click.option('--rds-instances', is_flag=True, help='Delete RDS instances.')
@click.pass_context
def main(ctx, force, all, s3_buckets, ec2_instances, cloudwatch_logs, kms_keys, rds_instances):
    
    # Default to dry run unless --force is specified
    dry_run = not force

    # Show help if no options are provided
    if not any([force, all, s3_buckets, ec2_instances, cloudwatch_logs, kms_keys, rds_instances]):
        click.echo(ctx.get_help())
        ctx.exit()

    # If --all is specified, set all resource options to True
    if all:
        s3_buckets = ec2_instances = cloudwatch_logs = kms_keys = rds_instances = True

    if s3_buckets:
        perform_deletion("S3 bucket", list_s3_buckets, delete_s3_bucket, dry_run)
    
    if ec2_instances:
        perform_deletion("EC2 instance", list_ec2_instances, delete_ec2_instance, dry_run)
    
    if cloudwatch_logs:
        perform_deletion("CloudWatch log group", list_cloudwatch_logs, delete_cloudwatch_log, dry_run)
    
    if kms_keys:
        perform_deletion("KMS key", list_kms_keys, delete_kms_key, dry_run)
    
    if rds_instances:
        perform_deletion("RDS instance", list_rds_instances, delete_rds_instance, dry_run)

if __name__ == "__main__":
    # Ensure environment variables are set before running the script
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        raise EnvironmentError("AWS credentials are not set in environment variables.")
    
    main()
