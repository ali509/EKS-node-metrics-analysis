# Kubernetes Node Metrics Cronjob

**This project aims to create a Kubernetes cronjob that pulls node metrics such as CPU, memory, and disk usage from Kubernetes nodes and stores them in individual files.** 

1. To collect and expose metrics, we utilize **Node Exporter**, a Prometheus exporter for hardware and OS metrics.
2. The **Kubernetes cronjob** designed to run at regular intervals, creating a new file with a timestamp each time it executes. 
3. The solution is implemented using **Python scripting** for the cron job, Docker for containerization, and Kubernetes YAML deployment.
4. **Persistent Volume Claim (PVC)** for storing the files generated by cronjob ensuring the data is retained even on pod restarts.

The deployment can be performed on a local Kubernetes setup like Minikube or Kind, or on a cloud platform’s Kubernetes flavor (e.g., EKS). Here, I have used **EKS (Elastic kubernetes service)**. This document provides a step-by-step guide on the design, deployment, and usage of the solution, along with the necessary code and configuration files. 

## Directory Structure of files :

<img width="289" alt="image" src="https://github.com/ali509/EKS-node-metrics-analysis/assets/39634565/93518bb0-7d43-468b-a271-ae9ede4fb7f5">


## Prerequisites

- **Metric Server:**
  - **Purpose:** Collects resource metrics for pods and nodes.
- **EBS CSI Driver Addon:**
  - **Purpose:** Manages Amazon EBS volumes for persistent storage.
- **Bastion Server:**
  - **Purpose:** Acts as a secure access point to the Kubernetes cluster.
- **Python:**
  - **Purpose:** Used for scripting and automation.

## Files and Configuration

### Dockerfile

Defines the steps to build a Docker image.
Images are pushed to Docker Hub.

### Python Scripts

- **python_script.py:** Responsible for collecting node metrics, filtering, and storing them in files.
- **requirements.txt:** Contains dependencies required by the Python script.

### Manifest Files

- **cron.yaml:** Defines a Kubernetes cron job scheduled to run at regular intervals. It executes the Python script to collect node metrics and store them in files.
- **nodemetrics.yaml:** YAML file for pod creation to store log files generated by the Kubernetes cron job.
- **pvc.yaml:** YAML file defining a Persistent Volume Claim (PVC) used for storing metric data persistently.

### Node Exporter

- **configmap.yaml:** Configures Node Exporter.
- **daemonset.yaml:** Deploys Node Exporter as a DaemonSet on all nodes in the Kubernetes cluster.
- **load_balancer.yaml:** Contains resources for load balancing or exposing Node Exporter metrics externally.

## Deployment Steps

1. **Build and Push Image to Docker Hub:**
   - Use the provided Dockerfile to build a Docker image containing the necessary components, including the Python script and any dependencies.
   - Push the Docker image to Docker Hub for deployment in Kubernetes.

2. **Apply Manifest Files:**
   - Use the `kubectl apply` command to apply the manifest files located in the project directory.
   - Apply the `PVC.yaml` file to claim storage for metric data persistence.
   - Apply the `cronjob.yaml` file to schedule the execution of the Python script for collecting node metrics.
   - Apply any additional manifest files, such as those for Node Exporter or other related resources.

3. **Sanity Checking:**
   - After applying the manifest files, use `kubectl get pods` to check the status of pods and ensure they are all in the Running state.
   - Inspect pod logs using `kubectl describe pod` to debug any issues if pods are not running correctly.

4. **Debugging and Logging:**
   - If any pods encounter issues, inspect the logs of the relevant pods using `kubectl logs`.
   - Resolve any errors reported in the logs to identify and fix potential deployment issues.

5. **Access Node Exporter URL:**
   - Once all pods are running successfully, access the URL of Node Exporter to verify that it is exposing metrics correctly.
   - Open a web browser and navigate to the Node Exporter URL (typically in the format `http://<node-exporter-ip>:<port>/metrics`).
   - Verify that metrics are being exposed and can be accessed from the Node Exporter endpoint.

      <img width="619" alt="image" src="https://github.com/ali509/EKS-node-metrics-analysis/assets/39634565/df6e5de1-5f30-4e01-bb68-9bec73b32c00">
      <img width="656" alt="image" src="https://github.com/ali509/EKS-node-metrics-analysis/assets/39634565/08bac891-44f3-4579-9b8a-7993576ea1dd">


6. **Validation and Monitoring:**
   - Validate the functionality of the cron job by checking that metric data is being collected and stored persistently in the PVC.
   - Log in to the pod created using `nodemetrics.yaml`.

       <img width="555" alt="image" src="https://github.com/ali509/EKS-node-metrics-analysis/assets/39634565/c0105acb-aa14-420d-82e9-bbda5ab5e0b9">
