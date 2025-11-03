# Multi-Admin System with Role-Based Access Control

## Overview

The ServiceHub platform now includes a comprehensive multi-admin system with role-based access control (RBAC). This system allows you to create multiple administrators with different permission levels and manage them effectively.

## Admin Roles and Permissions

### 1. Super Admin (`super_admin`)
**Full system access - can do everything**
- Create, edit, and delete other admins
- Access all financial data and reports  
- Manage all content and policies
- Full user management capabilities
- Complete system administration

### 2. Finance Admin (`finance_admin`)
**Financial management focus**
- View financial data and reports
- Manage wallet funding requests
- Edit job access fees
- View payment proofs
- Generate financial reports
- **Cannot**: Manage other admins, delete users

### 3. Content Admin (`content_admin`)
**Content and job management focus**
- Manage job postings and approvals
- Edit policies and contact information
- Manage locations and trade categories
- Configure job questions
- **Cannot**: Access financial data, manage users, manage admins

### 4. User Admin (`user_admin`)
**User management focus**
- View and manage user accounts
- Handle user verifications
- Manage user statuses
- **Cannot**: Access financial data, manage jobs, manage admins

### 5. Support Admin (`support_admin`)
**Customer support focus**
- Manage notifications and communications
- Handle support tickets
- Send notifications to users
- View user data for support purposes
- **Cannot**: Manage finances, delete users, manage admins

### 6. Read-Only Admin (`read_only_admin`)
**View-only access for reporting**
- View financial reports (read-only)
- View user statistics (read-only)
- View system statistics (read-only)
- **Cannot**: Make any changes to the system

## Getting Started

### Initial Setup

1. **Default Super Admin**: The system creates a default super admin account during the first login with legacy credentials (`admin`/`servicehub2024`)

2. **First Login**: Use the legacy credentials to access the system, which will create the default super admin account.

3. **Create Additional Admins**: Once logged in as super admin, navigate to the "Admin Management" tab to create additional administrators.

### Creating New Admins

1. **Navigate to Admin Management**:
   - Log in to the admin dashboard
   - Click on the "Admin Management" tab (👨‍💼)

2. **Add New Admin**:
   - Click "Add Admin" button
   - Fill in the required information:
     - Username (unique)
     - Email address
     - Full name
     - Role (select appropriate role)
     - Phone (optional)
     - Notes (optional)

3. **Temporary Password**:
   - The system generates a secure temporary password
   - The new admin must change this password on first login
   - In production, the password would be sent via email

### Managing Existing Admins

#### View Admin List
- See all administrators with their roles and status
- View last login information and login counts
- Filter by role or status

#### Edit Admin Details
- Update admin information (email, name, phone)
- Change admin roles (if you have permission)
- Update status (active/inactive)

#### Reset Passwords
- Reset forgotten passwords for other admins
- Generate new secure passwords
- Force password change on next login

#### Delete/Deactivate Admins
- Soft delete (deactivate) admin accounts
- Cannot delete your own account
- Cannot delete super admins (unless you're a super admin)

## Role Hierarchy and Permissions

### Permission System
The system uses a role-based permission system where each role has specific permissions:

```
Super Admin (Level 5)
├── Finance Admin (Level 4)
├── Content Admin (Level 3)
├── User Admin (Level 2)
├── Support Admin (Level 2)
└── Read-Only Admin (Level 1)
```

### Management Rules
- Higher level roles can manage lower level roles
- Admins cannot manage other admins of the same or higher level
- Super Admin can manage all roles
- Finance Admin can manage Content, User, Support, and Read-Only admins
- Other roles cannot manage admins

## Security Features

### Authentication & Security
- **JWT-based authentication** with 8-hour expiration
- **Password complexity requirements** (minimum 8 characters)
- **Account lockout** after 5 failed login attempts (30-minute lockout)
- **Forced password changes** for new accounts and resets
- **Secure password hashing** using bcrypt

### Activity Logging
- All admin actions are logged with:
  - Admin username and ID
  - Action type and description
  - Target entity (user, job, etc.)
  - IP address and user agent
  - Timestamp
  - Additional metadata

### Session Management
- **JWT tokens** with expiration
- **Automatic logout** after token expiration
- **Session tracking** with login counts

## API Endpoints

### Admin Management Endpoints

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| POST | `/api/admin-management/login` | Admin login | Public |
| GET | `/api/admin-management/me` | Get current admin info | Any Admin |
| GET | `/api/admin-management/admins` | List all admins | Super Admin |
| POST | `/api/admin-management/admins` | Create new admin | Super Admin |
| PUT | `/api/admin-management/admins/{id}` | Update admin | Super Admin |
| DELETE | `/api/admin-management/admins/{id}` | Delete admin | Super Admin |
| POST | `/api/admin-management/admins/{id}/reset-password` | Reset password | Super Admin |
| GET | `/api/admin-management/roles` | Get available roles | Any Admin |
| GET | `/api/admin-management/activity` | Get activity logs | Super Admin |
| GET | `/api/admin-management/stats` | Get admin statistics | Super Admin |

### Authentication Headers
All API requests (except login) require authentication:
```
Authorization: Bearer <jwt_token>
```

## Usage Examples

### Creating a Finance Admin
```javascript
const financeAdmin = {
  username: "john_finance",
  email: "john@servicehub.co",
  full_name: "John Smith",
  role: "finance_admin",
  phone: "+234-123-456-7890",
  notes: "Handles all financial operations"
};

// API call to create admin
const response = await fetch('/api/admin-management/admins', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${adminToken}`
  },
  body: JSON.stringify(financeAdmin)
});
```

### Checking Permissions
```javascript
// Get current admin info with permissions
const adminInfo = await fetch('/api/admin-management/me', {
  headers: { 'Authorization': `Bearer ${adminToken}` }
});

const { admin, permissions } = await adminInfo.json();

// Check if admin can manage finances
const canManageFinances = permissions.includes('manage_wallet_funding');
```

## Best Practices

### Security
1. **Regular Password Changes**: Encourage admins to change passwords regularly
2. **Principle of Least Privilege**: Give admins only the permissions they need
3. **Regular Access Reviews**: Periodically review admin access and roles
4. **Monitor Activity Logs**: Regularly check admin activity for suspicious behavior

### Organization
1. **Clear Role Definitions**: Ensure each admin understands their role and limitations
2. **Documentation**: Keep records of who has what access and why
3. **Backup Super Admin**: Always have at least two super admin accounts
4. **Regular Cleanup**: Remove inactive admin accounts

### Operational
1. **Training**: Train admins on their specific interfaces and responsibilities
2. **Communication**: Establish clear communication channels for admin coordination
3. **Escalation**: Define escalation paths for issues requiring higher permissions

## Troubleshooting

### Common Issues

**1. Login Issues**
- Check if account is active
- Verify password hasn't expired
- Check for account lockout (wait 30 minutes or reset)

**2. Permission Denied**
- Verify admin role has required permissions
- Check if trying to manage higher-level admin
- Confirm JWT token is valid and not expired

**3. Cannot Create Admins**
- Only Super Admins can create other admins
- Check if username/email already exists
- Ensure all required fields are provided

**4. Password Reset Issues**
- Only Super Admins can reset passwords
- Cannot reset your own password via admin interface
- Use the "change password" option for self-service

### Database Collections

The admin system uses these MongoDB collections:
- `admins` - Admin account information
- `admin_activities` - Activity logs

### Environment Variables
Ensure these are properly configured:
- `MONGO_URL` - Database connection
- `JWT_SECRET` - For token signing (use environment variable in production)

## Migration from Single Admin

If you're upgrading from the single admin system:

1. **First Login**: Use existing credentials (`admin`/`servicehub2024`)
2. **Create Super Admin**: System automatically creates proper super admin account
3. **Add Team Members**: Create additional admin accounts as needed
4. **Update Processes**: Update operational procedures to use role-based access
5. **Training**: Train team members on their specific admin interfaces

## Production Deployment

### Security Considerations
1. **JWT Secret**: Use a strong, random JWT secret key from environment variables
2. **HTTPS**: Ensure all admin access is over HTTPS
3. **Email Integration**: Set up email service for password notifications
4. **Backup**: Regular backups of admin accounts and activity logs
5. **Monitoring**: Monitor admin activities and login patterns

### Performance
- Admin endpoints are optimized for typical admin workloads
- Activity logs are indexed for fast searching
- Pagination is implemented for large datasets

This multi-admin system provides the flexibility and security needed for a growing platform while maintaining ease of use for administrators at all levels.