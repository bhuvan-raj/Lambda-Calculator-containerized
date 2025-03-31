
# **Lambda Calculator Project**  

## **About the Project**  
A containerized web calculator deployed as an **AWS Lambda function** with a frontend UI.  
- **Backend**: Python (Flask) running in a Lambda container  
- **Frontend**: HTML/CSS (CSS hosted on **S3** due to Lambda limitations)  
- **Deployment**: Docker → ECR → Lambda with Function URL  

---

## **File Directory Tree**  
```
lambda-calc/  
├── app.py                # Flask backend (Lambda handler)  
├── Dockerfile            # Container setup  
├── requirements.txt      # Python dependencies  
├── static/  
│   └── styles.css        # CSS (hosted on S3)  
└── templates/  
    └── index.html        # Frontend HTML  
```

---

## **Prerequisites**  
✅ **AWS Account** (with permissions for Lambda, ECR, S3)  
✅ **AWS CLI** configured (`aws configure`)  
✅ **Docker** installed  

---

## **Step-by-Step Setup**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/bhuvan-raj/Lambda-Calculator-containerized.git
cd Lambda-Calculator-containerized
```

---

### **2. Upload CSS to S3 (AWS Console)**  
1. Go to **S3 Console** → **Create Bucket** (e.g., `lambda-calculator-assets`)  
2. Upload `static/styles.css`  
3. Set **Permissions**:  
   - **Bucket Policy**: Allow public reads  
   - **Object ACL**: Enable "Public Read"  
4. Update `templates/index.html` to reference S3:  
   ```html
   <link rel="stylesheet" href="https://lambda-calculator-assets.s3.amazonaws.com/styles.css">
   ```

---

### **3. Build Docker Image**  
```bash
docker build --platform linux/amd64 -t calculator-lambda .
```

---

### **4. Push to AWS ECR (CLI)**  
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repo (if not exists)
aws ecr create-repository --repository-name calculator-lambda

# Tag and push
docker tag calculator-lambda:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/calculator-lambda:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/calculator-lambda:latest
```

---

### **5. Deploy Lambda (AWS Console)**  
1. **Lambda Console** → **Create Function** → **Container Image**  
2. Select the pushed ECR image (`calculator-lambda:latest`)  
3. **Configuration**:  
   - **Memory**: 512MB  
   - **Timeout**: 30 sec  

---

### **6. Enable Function URL**  
1. In Lambda → **Configuration** → **Function URL**  
2. **Auth Type**: `NONE` (for public access)  
3. **Save URL** (e.g., `https://<id>.lambda-url.us-east-1.on.aws/`)  

---

## **License**  
**MIT License** - See [LICENSE](LICENSE).  

---

### **Troubleshooting**  
🔹 **CSS not loading?** → Verify S3 bucket permissions (`public-read`)  
🔹 **Lambda timeout?** → Increase timeout in configuration  
🔹 **Docker build issues?** → Use `--no-cache` and rebuild  

---
