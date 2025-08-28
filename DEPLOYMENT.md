# 🚀 Deployment Guide

## GitHub Repository Deployment

This guide will help you deploy the Urban Micro-Climate Map project to your GitHub repository.

## 📋 Prerequisites

- GitHub account
- Git installed on your local machine
- VS Code or any code editor
- Docker (for local testing)

## 🔧 Step-by-Step Deployment

### 1. Clone Your Repository

```bash
git clone https://github.com/Chirag935/Project-1.git
cd Project-1
```

### 2. Copy Project Files

Copy all the project files from this workspace to your cloned repository directory.

### 3. Initialize Git and Add Files

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Urban Micro-Climate Map implementation"

# Add remote origin
git remote add origin https://github.com/Chirag935/Project-1.git

# Push to main branch
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to your GitHub repository: https://github.com/Chirag935/Project-1
2. Click on **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Choose **gh-pages** branch
6. Click **Save**

### 5. Enable GitHub Actions

1. In your repository, click on **Actions** tab
2. Click **Enable Actions**
3. The workflow will automatically run on your next push

## 🌐 Access Your Deployed Application

After deployment, your application will be available at:
```
https://chirag935.github.io/Project-1/
```

## 🔄 Updating the Application

To update your deployed application:

```bash
# Make your changes
# Then commit and push
git add .
git commit -m "Update: [describe your changes]"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Test the backend
2. Test the frontend
3. Build the frontend
4. Deploy to GitHub Pages

## 🐛 Troubleshooting

### Issue: GitHub Actions not running
- Check if Actions are enabled in your repository
- Verify the workflow file is in `.github/workflows/` directory
- Check the Actions tab for error messages

### Issue: Build failures
- Check the Actions logs for specific error messages
- Verify all dependencies are correctly specified
- Test locally before pushing

### Issue: GitHub Pages not updating
- Wait a few minutes for deployment to complete
- Check the Actions tab for deployment status
- Verify the gh-pages branch exists

## 📱 Local Development

For local development, use the provided scripts:

```bash
# Development mode
./run-dev.sh

# Production mode with Docker
./start.sh
```

## 🔒 Security Notes

- The deployed frontend will be publicly accessible
- Backend services are not deployed (only frontend)
- Consider using environment variables for sensitive data
- Enable branch protection rules for main branch

## 📊 Monitoring

- Check GitHub Actions for build/deployment status
- Monitor repository insights for traffic and usage
- Set up notifications for failed deployments

## 🎯 Next Steps

After successful deployment:

1. **Customize the application** for your specific needs
2. **Add real webcam URLs** to the backend
3. **Implement user authentication** if required
4. **Add monitoring and logging**
5. **Scale the backend** for production use

## 📞 Support

If you encounter issues:

1. Check the GitHub Actions logs
2. Review the troubleshooting section
3. Check the project documentation
4. Open an issue in your repository

---

**🎉 Congratulations!** Your Urban Micro-Climate Map is now deployed and accessible to the world!