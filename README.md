# 🐨 KOALASPOTTR Workshop

## 📝 Workshop Steps

### Part 1: Setup Your Environment (10 minutes)

#### Step 1: Create Your S3 Bucket

1. Open the **AWS Console** → Go to **S3**
2. Click **Create bucket**
3. Bucket name: `firstname-lastname-koala-bucket` (replace with your name)
   - Example: `alexander-sneyers-koala-bucket`
4. Region: `eu-central-1` (Europe - Frankfurt)
5. **Block all public access**: ✅ Keep enabled (security best practice)
6. Click **Create bucket**

#### Step 2: Configure CORS on Your Bucket

1. Go to your bucket → **Permissions** tab
2. Scroll to **Cross-origin resource sharing (CORS)**
3. Click **Edit**
4. Copy the contents from `config/cors-configuration.json` in this repository
5. Paste into the CORS configuration editor
6. Click **Save changes**

---

### Part 2: Deploy the Lambda Function (15 minutes)

#### Step 3: Create Lambda Function

1. Go to **AWS Lambda** → Click **Create function**
2. Choose **Author from scratch**
3. Function name: `firstname-lastname-KoalaSpottrProcessor`
   - Example: `alexander-sneyers-KoalaSpottrProcessor`
4. Runtime: **Python 3.12**
5. Architecture: **x86_64**
6. Expand **Change default execution role**
7. Select **Use an existing role**
8. Choose: **Koala-Verification-Agent-role**
9. Click **Create function**

#### Step 4: Configure Lambda

1. In the **Code** tab, replace the default code with the code from `lambda/lambda_function.py`
2. Click **Deploy**
3. Click **Configuration** → **Environment variables** → **Edit**
4. Click **Add environment variable**
5. Set:
   - Key: `RECIPIENT_PHONE`
   - Value: Your phone number in E.164 format (example: `+32470123456`)
6. Click **Save**

#### Step 5: Verify Lambda Permissions

The existing **Koala-Verification-Agent-role** should already have these policies:
- ✅ `AmazonS3ReadOnlyAccess`
- ✅ `AmazonRekognitionFullAccess`
- ✅ `AmazonSNSFullAccess`

To verify:
1. Go to **Configuration** → **Permissions**
2. Click on the role name **Koala-Verification-Agent-role**
3. Confirm the policies are attached

#### Step 6: Add S3 Trigger

1. In Lambda, click **Add trigger**
2. Select **S3**
3. Bucket: Select your `firstname-lastname-koala-bucket`
4. Event type: **All object create events**
5. Acknowledge the warning
6. Click **Add**

---

### Part 3: Upload Your First Koala Image (10 minutes)

#### Step 7: Download the Upload Page

1. Download `KoalaSpottrFrontEnd.html` from this repository
2. Save it to your computer
3. **Double-click** to open it in your browser

#### Step 8: Generate Presigned Upload URL

1. Open **AWS CloudShell** (click the `>_` icon in AWS Console top bar)
2. Wait for CloudShell to initialize (~10 seconds)
3. Use the command from `scripts/generate-upload-url.txt` in this repository
4. Replace `YOUR-BUCKET-NAME` with your actual bucket name
5. Press **Enter**
6. Copy the **entire long URL** that's output

#### Step 9: Upload Your Image

1. Go back to the **KoalaSpottrFrontEnd.html** page in your browser
2. **Paste the presigned URL** in STEP 1
3. Click **"Set Upload URL"**
4. **Select or drag & drop** your koala image in STEP 2
5. Click **"Upload 🚀"**
6. Wait for the success message!

#### Step 10: Check Your SMS

Within 10-15 seconds, you should receive an SMS with:
- ✅ **"KOALA DETECTED!"** if it's a koala
- ❌ **"NOT A KOALA!"** if it's not a koala

---

## 🐨 Happy Koala Spotting!
