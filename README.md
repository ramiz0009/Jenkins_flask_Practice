# Jenkins CI/CD Pipeline for Flask Student Management Application

A complete CI/CD pipeline setup for a Flask-based student management application using Jenkins, GitHub webhooks, and automated testing.

## Installation

### VM Setup

Update your VM and install required dependencies:

```bash
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install MongoDB
sudo apt install -y mongodb

# Start and enable MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify MongoDB
sudo systemctl status mongodb
```

### Jenkins Setup

#### Install Java

```bash
sudo apt install -y openjdk-11-jdk

# Verify installation
java -version
```

#### Install Jenkins

```bash
# Add Jenkins repository
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

# Install and start Jenkins
sudo apt update
sudo apt install -y jenkins

sudo systemctl start jenkins
sudo systemctl enable jenkins

# Check status
sudo systemctl status jenkins
```

#### Access Jenkins

1. Navigate to `http://your-vm-ip:8080`
2. Retrieve the initial admin password:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
   -<img width="940" height="107" alt="image" src="https://github.com/user-attachments/assets/7db65753-e758-419b-9f50-fd06d5ae4818" />

3. Complete the setup wizard and install recommended plugins
   - <img width="940" height="548" alt="image" src="https://github.com/user-attachments/assets/0a132758-dff7-4a72-b16d-6f4336803251" />
   - <img width="940" height="453" alt="image" src="https://github.com/user-attachments/assets/c585c3a8-8077-49b4-a1f4-b13a9c5c3f4f" />



### Repository Setup

Clone the repository into your VM:

```bash
git clone https://github.com/ramiz0009/Jenkins_flask_Practice.git
cd Jenkins_flask_Practice
```
-<img width="940" height="78" alt="image" src="https://github.com/user-attachments/assets/635785bf-ca60-4eb5-81c2-ddcf006b03df" />


**Now go inside the cloned repo and create our Jenkinsfile, test file and update our requirement.txt**
- `Jenkinsfile` - Pipeline configuration
- `requirements.txt` - Python dependencies
- `test_*.py` - Unit test files

## Configuration

### GitHub Webhooks

Set up automatic build triggers when code is pushed:

1. Go to your GitHub repository
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Configure as follows:
   - **Payload URL:** `http://your-vm-ip:8080/github-webhook/`
   - **Content type:** `application/json`
   - **Which events:** Select "Just the push event"
   - **Active:** Check the box
4. Click **Add webhook**
- <img width="940" height="595" alt="image" src="https://github.com/user-attachments/assets/abaaff21-1ba9-419a-97c5-c6a85c8ecd4a" />

### Email Notifications

#### Configure SMTP for Extended Email Notifications

1. Go to **Manage Jenkins** → **Configure System**
2. Scroll to **Extended E-mail Notification**
3. Set the following:
   - **SMTP server:** `smtp.gmail.com`
   - **SMTP Port:** `465`
   - Check **Use SSL**
   - Add Jenkins credentials
4. Click **Save**
- <img width="940" height="533" alt="image" src="https://github.com/user-attachments/assets/744ae072-6fe8-42f3-a6fa-f10e4bceb046" />

#### Configure Default Email Settings

1. In **Configure System**, scroll to **E-mail Notification**
2. Set the following:
   - **SMTP server:** `smtp.gmail.com`
   - **User Name:** Your Gmail address
   - **Password:** Your Google app password (not regular password)
   - **SMTP Port:** `465`
   - Check **Use SMTP Authentication**
   - Check **Use SSL**
   - **Reply-To Address:** Your Gmail address
   - <img width="940" height="271" alt="image" src="https://github.com/user-attachments/assets/3c4f2553-6fb5-4fde-91b6-8a246d6f5507" />

3. Click **Test configuration** to send a test email
4. Click **Save**
   - <img width="940" height="328" alt="image" src="https://github.com/user-attachments/assets/39eab976-31f7-49cc-b852-ac29c230d85f" />

### Jenkins Credentials

#### Add MongoDB URI Credential

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** domain
3. Click **Add Credentials**
4. Configure as follows:
   - **Kind:** Secret text
   - **Scope:** Global
   - **Secret:** `mongodb+srv://username:password@cluster.mongodb.net/student_db?retryWrites=true&w=majority`
   - **ID:** `MONGO_URI`
   - **Description:** MongoDB Connection String
5. Click **OK**
 - <img width="940" height="350" alt="image" src="https://github.com/user-attachments/assets/0a24d08f-24a4-4be2-8e0f-97074c16de36" />

#### Add Flask Secret Key Credential

1. Repeat the above steps with:
   - **Kind:** Secret text
   - **Scope:** Global
   - **Secret:** Your random secret key
   - **ID:** `SECRET_KEY`
   - **Description:** Flask Secret Key
2. Click **OK**
 - <img width="940" height="363" alt="image" src="https://github.com/user-attachments/assets/928e1848-ba5c-4b14-8859-dd77f2e9ee59" />

### Pipeline Setup

1. Go to Jenkins Dashboard
2. Click **New Item**
3. Enter name: `Flask-Student-App-Pipeline`
4. Select **Pipeline**
5. Click **OK**

#### Configure General Settings

- **Description:** CI/CD Pipeline for Flask Student Management Application
- Check **GitHub project**
- **Project URL:** `https://github.com/ramiz0009/Jenkins_flask_Practice`
 - <img width="940" height="503" alt="image" src="https://github.com/user-attachments/assets/b104bec8-b405-4071-946d-1b8a7f1dfb85" />

#### Configure Build Triggers

- Check **GitHub hook trigger for GITScm polling**
- <img width="940" height="250" alt="image" src="https://github.com/user-attachments/assets/6059f92a-e589-4809-a907-299b139fd67c" />

#### Configure Pipeline

- **Definition:** Pipeline script from SCM
- **SCM:** Git
- **Repository URL:** `https://github.com/ramiz0009/Jenkins_flask_Practice.git`
- **Credentials:** Leave as none if public repo
- **Branch Specifier:** `*/main`
- **Script Path:** `Jenkinsfile`
- <img width="940" height="521" alt="image" src="https://github.com/user-attachments/assets/a4caf6d8-1352-42c9-b89d-23460d54695a" />

Click **Save**

## Usage

The pipeline is automatically triggered when you push changes to the main branch:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```
- <img width="940" height="478" alt="image" src="https://github.com/user-attachments/assets/99c180e4-3d82-4085-9879-c092ab884817" />

**Our build is triggered and pipeline is working successfully**
- <img width="940" height="567" alt="image" src="https://github.com/user-attachments/assets/d066329a-6e61-4a37-8820-9e5f0abb64f6" />
- <img width="940" height="359" alt="image" src="https://github.com/user-attachments/assets/3baa9555-c4d8-4f32-bf49-a2daff02bac0" />


Jenkins will:
1. Detect the webhook trigger
2. Clone the latest code
3. Run unit tests
4. Build the application
6. Send email notifications on success or failure
   - <img width="940" height="472" alt="image" src="https://github.com/user-attachments/assets/4e9c694c-a614-43ee-8fc7-e3dda4422a71" />

8. Deploy the application

## Application Access

Once the pipeline completes successfully, access your Flask application at:

```
http://your-vm-ip:8000/
```
- <img width="940" height="268" alt="image" src="https://github.com/user-attachments/assets/0898b0b1-9b95-41b6-a05e-dc84e3dae538" />
- <img width="940" height="361" alt="image" src="https://github.com/user-attachments/assets/4f56aca1-ac2f-494e-946a-e9d776bf6e96" />

