# Deployment and Kubernetes Management Guide

## Docker Commands

### Build Docker Image (No Cache)
```bash
docker build --no-cache -t dellaxy/image_name:latest -f Dockerfile .
```

### Push Image to Registry
```bash
docker push dellaxy/image_name:latest
```

### Run Docker Container
```bash
docker run -p 8080:80 dellaxy/frontend:latest
```

---

## Kubernetes Commands (Namespace: `exam-richard`)

### View All Pods
```bash
kubectl get pods -n exam-richard
```

### Describe a Specific Pod
```bash
kubectl describe pod <pod_name> -n exam-richard
```

### Restart a Deployment
```bash
kubectl rollout restart deployment/<deployment_name> -n exam-richard
```

### Delete a Deployment
```bash
kubectl delete deployment exam-richard-deployment-be -n exam-richard
```

---

## Persistent Volume (PV) / Persistent Volume Claim (PVC) Management

> ⚠️ **Important:** When editing or deleting PV/PVC, ensure all pods and deployments using them are deleted **before** removing the PV/PVC itself.

### Delete All Resources in Namespace
```bash
kubectl delete all --all -n exam-richard
```

### Delete All PVCs
```bash
kubectl delete pvc --all -n exam-richard
```

### Delete All ConfigMaps
```bash
kubectl delete configmap --all -n exam-richard
```

### Delete All Secrets
```bash
kubectl delete secret --all -n exam-richard
```
