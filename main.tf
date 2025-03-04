# Specify the Terraform version and provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.4.0"
}

provider "aws" {
  region = "us-east-1" # Change to your preferred AWS region
}

# Elastic Beanstalk Application
resource "aws_elastic_beanstalk_application" "marketplace" {
  name        = "marketplace"
  description = "Flask web application hosted on Elastic Beanstalk"
}

# Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "marketplace_env" {
  name                = "marketplace-env"
  application         = aws_elastic_beanstalk_application.marketplace.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.4.0 running Python 3.12"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.micro"
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance"
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "serviceRole"
    value     = "aws-elasticbeanstalk-service-role"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "marketplace-ec2-role"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "DisableIMDSv1"
    value     = "true"
  }


}

# S3 Bucket for Application Version Storage
resource "aws_s3_bucket" "flask_app_bucket" {
  bucket = "flask-app-version-${var.project_suffix}"

  tags = {
    Name        = "flask-app-bucket"
    Environment = "Dev"
  }
}

# Elastic Beanstalk Application Version
resource "aws_elastic_beanstalk_application_version" "marketplace_version" {
  application = aws_elastic_beanstalk_application.marketplace.name
  bucket      = aws_s3_bucket.flask_app_bucket.bucket
  key         = "${var.flask_app_zip}"
  name        = "v1"
}

# Variables
variable "project_suffix" {
  description = "Unique suffix for resources to avoid naming conflicts"
  type        = string

}

variable "flask_app_zip" {
  description = "Path to the Flask application zip file"
  type        = string
}

# Outputs
output "application_name" {
  value = aws_elastic_beanstalk_application.marketplace.name
}

output "environment_url" {
  value = aws_elastic_beanstalk_environment.marketplace_env.endpoint_url
}
