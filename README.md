# fastapi_cloud_healthcheck

A lightweight and flexible health check package for FastAPI applications, specifically designed for cloud services on AWS and Azure. It enables users to implement and expand health checks tailored to their service requirements with ease.

Utilizing Boto3 and Azure SDK for Python, this module allows for custom logic creation for various cloud services, including S3 buckets and Azure Blob storage. While it does not include built-in service checkers, it offers a straightforward framework for users to add their own, ensuring minimal dependency bloat by allowing only necessary packages.

## Installation
You can install the package using pip:

```bash
pip install fastapi-cloud-healthcheck
```

## Getting Started
Here’s a quick example to get you started with implementing health checks for your FastAPI application:

Before you start, make sure to install the required package by running:
```bash
pip install fastapi-cloud-healthcheck-aws-s3bucket
pip install fastapi-cloud-healthcheck-azure-vm
```
Then, you can use the following code in your FastAPI application:
```python
from fastapi import FastAPI
from fastapi_cloud_healthcheck import HealthCheckFactory, create_health_check_route
from fastapi_cloud_healthcheck_aws_s3bucket import HealthCheckS3Bucket
from fastapi_cloud_healthcheck_azure_vm import HealthCheckAzureVM

app = FastAPI()

# Create a factory for health checks
health_check_factory = HealthCheckFactory()

# Adding AWS S3 health check
health_check_factory.add(HealthCheckS3Bucket(
    bucket_name='my-test-bucket-1232424',
    region='us-east-1'
))

# Adding Azure VM Health Check
health_check_factory.add(HealthCheckAzureVM(
   vm_name="SampleTestVM",
   resource_group="Test-RG",
   subscription_id="12345678-1234-1234-1234-123456789abc",
   region="central-india"
))

# Adding health check route to the application
app.add_api_route('/health', endpoint=create_health_check_route(factory=health_check_factory), methods=["GET"])

# Start the FastAPI server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5000)
```

## Health Check Response
When you request a `/health` check, the module evaluates all submitted entries by running basic queries against them. The response will vary depending on the health of the services being checked.

### Success Response
If all checks return expected results, the response will include a status code of `200`, indicating a `healthy` state.

```json
{
  "systemHealth": {
    "status": "Healthy",
    "description": "All services are operating normally.",
    "statusCode": 200,
    "suggestion": "No action needed."
  },
  "totalResponseTime": "0:00:07.661384",
  "lastUpdated": "2024-10-03T07:14:02.188021+00:00",
  "summary": {
    "totalServices": 2,
    "healthyServices": 2,
    "unhealthyServices": 0,
    "warningServices": 0
  },
  "entities": [
    {
      "identifier": "my-test-bucket-1232424",
      "healthStatus": "Healthy",
      "statusCode": 200,
      "responseTime": "0:00:02.458496",
      "metadata": {
        "provider": "aws",
        "region": "us-east-1",
        "category": "storage",
        "serviceName": "S3",
        "accountId": "123456789101" 
      },
      "statusMessages": {
        "bucketCheck": "Bucket exists and is accessible.",
        "objectUpload": "Test object uploaded successfully.",
        "objectRead": "Test object content matches.",
        "cleanup": "Test object cleaned up successfully."
      }
    },
    {
      "identifier": "SampleTestVM",
      "healthStatus": "Healthy",
      "statusCode": 200,
      "responseTime": "0:00:05.202888",
      "metadata": {
        "provider": "azure",
        "region": "central-india",
        "category": "compute",
        "serviceName": "VM",
        "subscriptionId": "12345678-1234-1234-1234-123456789abc"
      },
      "statusMessages": {
        "powerStateCheck": "VM is running.",
        "diskHealthCheck": "All disks are healthy.",
        "networkInterfaceCheck": "All NICs are healthy."
      }
    }
  ]
}
```
### Failure Response
If any errors occur during the checks, the response will return a status code of `500`, indicating an `unhealthy` state.

```json
{
  "systemHealth": {
    "status": "Unhealthy",
    "description": "One or more services are not operating normally.",
    "statusCode": 500,
    "suggestion": "Please investigate the issues."
  },
  "totalResponseTime": "0:00:02.638861",
  "lastUpdated": "2024-10-03T07:20:01.254438+00:00",
  "summary": {
    "totalServices": 2,
    "healthyServices": 1,
    "unhealthyServices": 1,
    "warningServices": 0
  },
  "entities": [
    {
      "identifier": "my-test-bucket-1232424",
      "healthStatus": "Healthy",
      "statusCode": 200,
      "responseTime": "0:00:02.245721",
      "metadata": {
        "provider": "aws",
        "region": "us-east-1",
        "category": "storage",
        "serviceName": "S3",
        "accountId": "123456789101",
        "lastChecked": "2024-10-03T12:43:45.990525+05:30"
      },
      "statusMessages": {
        "bucketCheck": "Bucket exists and is accessible.",
        "objectUpload": "Test object uploaded successfully.",
        "objectRead": "Test object content matches.",
        "cleanup": "Test object cleaned up successfully."
      }
    },
    {
      "identifier": "SampleTestVM",
      "healthStatus": "Unhealthy",
      "statusCode": 500,
      "responseTime": "0:00:00.387757",
      "metadata": {
        "provider": "azure",
        "region": "central-india",
        "category": "compute",
        "serviceName": "VM",
        "subscriptionId": "12345678-1234-1234-1234-123456789abc"
      },
      "statusMessages": {
        "powerStateCheck": "VM is not running."
      }
    }
  ]
}
```

## Available Modules
Explore the available health check modules for this framework, designed to help you monitor the health of various services and systems:

* [fastapi_cloud_healthcheck_aws_s3bucket](https://github.com/yogeshselvarajan/fastapi-cloud-healthcheck-aws-s3bucket/blob/01cd0a494649aa0b580c03beaa3aedc24268da8b/fastapi_cloud_healthcheck_aws_s3bucket/bucket_check.py)
* [fastapi_cloud_healthcheck_azure_vm](https://github.com/yogeshselvarajan/fastapi_cloud_healthcheck_azure_vm/blob/6a6202348ad508ac8213d84eaf4ecb5ca6d619ee/fastapi_cloud_healthcheck_azure_vm/service.py)

If you've developed a public service module for this framework using any cloud service and would like to have it included in this list, please feel free to open a new issue in the repository. We will review your submission and add it to the list.

## Writing a Custom Module
You can easily extend the core health check module to support additional services by creating a custom module. Follow the steps below to build your own health check service:

1. **Implement the Interface**  
   Create a new service that implements the inherits the [HealthCheckBase](https://github.com/yogeshselvarajan/fastapi_cloud_healthcheck/blob/ac07ad1a6406520b28fd6b44e25daba6335434d5/fastapi_cloud_healthcheck/fastapi_cloud_healthcheck/services/base.py). It provides the necessary structure for integrating your custom health check.

2. **Build the Custom Class**  
   Design your class around the base class, implementing the required methods to define the health check logic at the ` __checkHealth__` function for your specific service based on the use case.

3. **Add to HealthCheckFactory**  
   Once your service is ready, integrate it into the `HealthCheckFactory` using the `main` file. This allows your custom health check to be easily used within the existing framework.

For a more concrete example, refer to the [fastapi_cloud_healthcheck_aws_s3bucket](https://github.com/yogeshselvarajan/fastapi-cloud-healthcheck-aws-s3bucket/blob/01cd0a494649aa0b580c03beaa3aedc24268da8b/fastapi_cloud_healthcheck_aws_s3bucket/bucket_check.py) module. It provides a detailed example of how to create and structure your own service to interface with the FastAPI health check system.

### Contributing

Once your custom module is ready, feel free to submit it to the repository by opening an issue. Your module could be added to the list of available health check modules.