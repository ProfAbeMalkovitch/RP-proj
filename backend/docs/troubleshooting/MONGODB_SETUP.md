# MongoDB Atlas Setup

Your MongoDB Atlas connection string has been configured.

## Connection Details

- **Username**: Research
- **Cluster**: students.jb1nyzd.mongodb.net
- **Database**: ilpg_db

## Setup Instructions

1. **Create .env file** (if not already created):
   - Navigate to the `backend` directory
   - Create a file named `.env`
   - Add the following content:

```
MONGODB_URI=mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority
DATABASE_NAME=ilpg_db
```

2. **Verify MongoDB Atlas Network Access**:
   - Go to your MongoDB Atlas dashboard
   - Navigate to Network Access
   - Ensure your IP address is whitelisted, or add `0.0.0.0/0` to allow all IPs (for development only)

3. **Initialize the Database**:
   ```bash
   cd backend
   python init_db.py
   ```

4. **Test the Connection**:
   - Start the backend server: `python main.py`
   - You should see "Successfully connected to MongoDB" in the console

## Important Notes

- The `.env` file is in `.gitignore` to protect your credentials
- Never commit your `.env` file to version control
- The connection string includes the database name (`ilpg_db`)
- The connection uses SSL/TLS (mongodb+srv://) which is required for MongoDB Atlas

## Troubleshooting

If you encounter connection errors:

1. **Check Network Access**: Ensure your IP is whitelisted in MongoDB Atlas
2. **Verify Credentials**: Double-check username and password
3. **Check Cluster Status**: Ensure your MongoDB Atlas cluster is running
4. **Check Firewall**: Ensure port 27017 (or 27017-27019) is not blocked

## Security Best Practices

For production:
- Use environment variables or a secrets manager
- Restrict network access to specific IPs
- Use database user with minimal required permissions
- Enable MongoDB Atlas authentication
- Use connection string with specific database name (already configured)









