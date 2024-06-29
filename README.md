# Bloopark Realestatex Complaints Module Documentation

## Module Overview

The Bloopark Realestatex Complaints module is designed to manage customer complaints for a real estate business. This module provides functionality to create, track, and manage complaints, assign them to users, and notify customers of the status of their complaints.

## Installation
- Install docker and docker compose
- Run docker using docker-compose up
- Create your database

### Module Installation

- Update the module list by going to `Apps` in the Odoo interface and clicking the `Update Apps List` button.
- Search for `Bloopark RealEstateX Complaints` in the `Apps` menu.
- Install the module by clicking the `Install` button.

## Configuration

### Assigning Users to Groups
- Go to `Settings > Users & Companies > Users`.
- Assign users to the `Complaint User` group to allow them to manage complaints also this group users will use for auto complaint assigns .
- Group Complaint User can see all complaint in company.


### Prepare outgoing mail server

- To test mail with complaint you must add outgoing mail server and make sure it's test passed

## Functionality

### Multi-company sequence

- There a hook that create a sequence for each company when module installed and this case handled in company creation after module install also to allow each company has their own sequence

### Auto Assign Lifecycle

- when you create a complaint you will find field Assigned-To readonly and empty thats because there an Automated action execute after 2 minutes of complaint creation time based on users in group ( Complaint User )

### Creating a Complaint
- Go to `Complaints > Complaints > Create`.
- Also from website you will find a new menu in the root menus called ( Complaints )
after create compalint from website and submit it will redirect to success page and there are a strong validation of fields also you can select in which company you want to add this complaint from website
- Fill in the complaint details such as title, email, address, type, and description.
- Save the complaint.

### Complaint Lifecycle
- complaint module installed with some default stages like below
- **New**: When a complaint is created, it starts in the `New` stage.
- **In Review**: For complaint review before start work on it.
- **In Progress**: After complaint review user can move it to in-progress.
- **Solved**: Once resolved, move the complaint to the `Solved` stage.
- **Dropped**: If a complaint is not valid or cannot be processed, move it to the `Dropped` stage.

### Automatic Email Notifications
- Email notifications are sent to customers when a complaint is created, moved to `Solved`, or `Dropped` stages.
- Email templates can be customized in `Settings > Technical > Email > Templates`.

### Access Control
- Users can only see complaints related to their assigned company.
- Multi-company support ensures data segregation and privacy.

## Advanced Features

### Stages Management
- Go to `Complaints > Stages` to manage different stages of complaints.
- Add or edit stages to fit your business process.

### Reporting
- Generate complaint reports by going to `Complaints > Print button near action button`.
- Customize report templates as needed.

## Testing

### Running Tests

- Tests are provided to ensure the module works correctly across different scenarios.
- To run the tests, use the following command in your Odoo installation directory:

  use below command in docker-compose file 
  `command: -d bloopark --test-enable -i bloopark_realestatex_complaints`
  Then run: `docker-compose up`
