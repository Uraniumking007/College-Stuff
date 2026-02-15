# Netflix (Subscription Based Model)

## Introduction

### Purpose

Service to provide movies and TV shows to users on a subscription basis to the users. Users can search for movies and TV shows, view details, add to watchlist, rate and review movies, and share on social media. Users can also stream movies in different resolutions, change audio and subtitle settings, and download movies for offline viewing. Users can make payment using UPI, cancel, renew, and upgrade their subscription.

### Product Scope

Scope of the product is to provide movies and TV shows to users on a subscription basis to the users. Users can search for movies and TV shows, view details, add to watchlist, rate and review movies, and share on social media. Users can also stream movies in different resolutions, change audio and subtitle settings, and download movies for offline viewing. Users can make payment using UPI, cancel, renew, and upgrade their subscription.

## Overall Description

### Product Perspective

The product is a web application that provides movies and TV shows to users on a subscription basis. The application will have a user-friendly interface that allows users to easily navigate and find the content they are looking for. The application will also have a robust backend that handles user authentication, movie database management, video streaming, and payment processing. The application will be built using modern web technologies and will be optimized for performance and scalability.

### User Classes and Characteristics

- Users: The primary users of the application will be individuals who are interested in watching movies and TV shows. They will expect a user-friendly interface that allows them to easily find and watch content.
- Administrators: The administrators will be responsible for managing the movie database, handling user accounts, and ensuring the smooth operation of the application. They will have access to a backend dashboard where they can perform these tasks.
- Content Providers: The content providers will be responsible for providing the movies and TV shows that will be available on the platform. They will have access to a content management system where they can upload and manage their content.
- Payment Processors: The payment processors will be responsible for handling the payment transactions for the subscriptions. They will have access to a payment gateway where they can process payments and manage subscriptions.

### Operating Environment

The application will be a web-based application that can be accessed from any modern web browser. The backend will be hosted on a cloud platform that provides scalability and reliability. The application will also have a mobile app version that can be accessed from iOS and Android devices.

### Design and Implementation Constraints

- The application must be built using modern web technologies such as React for the frontend and Node.js for the backend.
- The application must use a scalable database solution such as MongoDB or PostgreSQL to handle the movie database and user data.
- The application must integrate with a payment gateway that supports UPI payments for subscription management.
- The application must be optimized for performance and should have a load time of no more than 10 seconds.
- The application must have a backup server to handle traffic in case the primary server goes down, ensuring minimum downtime.
- The application must be designed to allow for maintenance without compromising service, with backup servers handling the load during maintenance periods.

### User Documentation

User documentation will be provided in the form of a user guide that will be accessible from within the application. The user guide will provide step-by-step instructions on how to use the various features of the application, including how to create an account, search for movies, add movies to the watchlist, stream movies, and manage subscriptions. Additionally, a FAQ section will be included to address common questions and issues that users may encounter.

### Assumptions and Dependencies

- The application assumes that users will have access to a stable internet connection to stream movies and manage their subscriptions.
- The application depends on third-party services for payment processing and content delivery, which may have their own limitations and constraints.
- The application assumes that users will have compatible devices and browsers to access the application and its features.
- The application depends on the availability of a robust backend infrastructure to handle user authentication, movie database management, video streaming, and payment processing.
- The application assumes that content providers will regularly update the movie database with new content to keep users engaged and subscribed to the service.
- The application depends on the availability of a backup server to ensure minimum downtime in case the primary server goes down or is under maintenance.

## External Interface Requirements

### User Interfaces

The user interface will be designed to be intuitive and user-friendly, allowing users to easily navigate through the application and access its features. The main components of the user interface will include:

- Home Page: The home page will display featured movies and TV shows, as well as personalized recommendations based on the user's viewing history.
- Search Page: The search page will allow users to search for movies and TV shows using various filters such as genre, release date, and rating.
- Movie Details Page: The movie details page will provide information about the movie, including synopsis, cast, crew, trailers, reviews, and ratings. Users will also have the option to add the movie to their watchlist, rate and review the movie, and share it on social media.
- Watchlist Page: The watchlist page will display the movies and TV shows that the user has added to their watchlist, allowing them to easily access and manage their saved content.
- Streaming Page: The streaming page will provide the interface for users to stream movies and TV shows, with options to pause, play, rewind, fast-forward, change audio and subtitle settings, and download movies for offline viewing.
- Subscription Management Page: The subscription management page will allow users to manage their subscriptions, including making payments, canceling, renewing, and upgrading their subscriptions.
- User Profile Page: The user profile page will allow users to view and edit their profile information, manage their account settings, and view their viewing history and preferences.
- Admin Dashboard: The admin dashboard will provide administrators with tools to manage the movie database, handle user accounts, and monitor the application's performance and usage.
- Content Management System: The content management system will allow content providers to upload and manage their movies and TV shows, including adding metadata, trailers, and other relevant information.

### Hardware Interfaces

The application will be designed to be accessed from a variety of devices, including desktop computers, laptops, tablets, and smartphones. The hardware requirements for accessing the application will include:

- A device with a modern web browser (e.g., Chrome, Firefox, Safari, Edge)
- A stable internet connection for streaming movies and managing subscriptions
- Sufficient storage space for downloading movies for offline viewing (optional)
- A compatible operating system (e.g., Windows, macOS, iOS, Android)

### Software Interfaces

The application will be built using modern web technologies, and will have the following software interfaces:

- Frontend: The frontend will be built using React, which will provide a responsive and interactive user interface for users to access the application's features.
- Backend: The backend will be built using Node.js, which will handle user authentication, movie database management, video streaming, and payment processing.
- Database: The application will use a scalable database solution like PostgreSQL to store user data, movie information, and subscription details.
- Payment Gateway: The application will integrate with a payment gateway that supports UPI payments for managing subscriptions and processing payments.
- Content Delivery Network (CDN): The application will use a CDN to efficiently deliver movie content to users, ensuring fast load times and a smooth streaming experience.

### Communication Interfaces

The application will communicate with various external services and APIs to provide its features. This will include:

- User Authentication API: The application will use an authentication API to handle user login, registration, password reset, and account recovery.
- Movie Database API: The application will use a movie database API to retrieve information about movies and TV shows, including details, trailers, reviews, and ratings.
- Payment Gateway API: The application will use a payment gateway API to process payments, manage subscriptions, and handle billing information.
- Content Delivery API: The application will use a content delivery API to efficiently deliver movie content to users, ensuring fast load times and a smooth streaming experience.
- Analytics API: The application will use an analytics API to track user behavior, monitor application performance, and gather insights to improve the user experience and optimize the service.

## System Features

### User Authentication

- Users will be able to create an account, log in, reset their password, recover their account, edit their profile data, deactivate/reactivate their account, and delete their account.

### User Profiles

- Users will be able to create and manage multiple user profiles, and protect profiles with a password.

### Movie Database

- Users will be able to search for movies, filter movies by genre, release date, rating, etc., view movie details (synopsis, cast, crew, etc.), view movie trailers, view movie reviews and ratings, add movies to their watchlist, rate and review movies, and share movies on social media.
- Administrators will be able to manage the movie database, including adding new movies, updating existing movies, and removing movies from the database.
- Content providers will be able to upload and manage their movies and TV shows, including adding metadata, trailers, and other relevant information.

### Video Streaming

- Users will be able to stream movies in different resolutions (SD, HD, 4K), pause, play, rewind, and fast-forward movies, change audio and subtitle settings, and download movies for offline viewing.

### Subscription Based Payment Gateway

- Users will be able to make payments using UPI, cancel their subscription, renew their subscription, and upgrade their subscription.

## Non-Functional Requirements

### Performance

- The application should be performant, with a load time of no more than 10 seconds.

### Minimum Downtime

- The downtime of the server should be minimum, and there should be a backup server to pick up traffic if the primary server goes down.

### Maintainability

- The server should be able to go into maintenance without compromising service, and backup servers should handle the load when the primary server is in maintenance.

### Scalability

- The application should be able to scale horizontally to handle increasing numbers of users and content without performance degradation.

### Security

- The application should implement robust security measures to protect user data, including encryption of sensitive information, secure authentication mechanisms, and regular security audits.
- User passwords should be stored securely using hashing algorithms.
- The application should comply with relevant data protection regulations to ensure user privacy.

### Usability

- The application should have an intuitive and user-friendly interface that allows users to easily navigate and access its features.
- The application should provide clear instructions and feedback to users to enhance their experience.

### Reliability

- The application should be reliable, with minimal downtime and a robust infrastructure to handle traffic and ensure continuous service availability.
- The application should have a backup and disaster recovery plan in place to ensure data integrity and availability in case of unexpected events.

## Cost Estimation (COCOMO Model)

### Overview

COCOMO (Constructive Cost Model) is a regression-based software cost estimation model that estimates effort (in person-months) and development time from an estimate of lines of source code (LOC). It supports three modes:

| Mode            | Project type                    | Characteristics                                      |
|-----------------|----------------------------------|------------------------------------------------------|
| **Organic**     | Small, simple, in-house         | Small team, familiar environment, flexible requirements |
| **Semi-detached** | Medium, mixed complexity       | Medium team, mixed experience, moderate innovation   |
| **Embedded**    | Large, complex, tight constraints | Rigid requirements, real-time/safety-critical aspects |

This project (subscription-based streaming platform with auth, streaming, payment, admin, and CMS) is classified as **Semi-detached**: medium size, mixed team experience, and moderate innovation.

### Basic COCOMO Formulas

**Effort (person-months):**

```
E = a × (KLOC)^b
```

**Development time (months):**

```
T = c × (E)^d
```

**Coefficients:**

| Mode          | a    | b     | c    | d     |
|---------------|------|-------|------|-------|
| Organic       | 2.4  | 1.05  | 2.5  | 0.38  |
| Semi-detached | 3.0  | 1.12  | 2.5  | 0.35  |
| Embedded      | 3.6  | 1.20  | 2.5  | 0.32  |

### Size Estimate (KLOC)

Based on the SRS scope:

| Component              | Estimated LOC | Notes                                                |
|------------------------|---------------|------------------------------------------------------|
| Frontend (React)       | 18,000        | UI, search, watchlist, streaming player, profiles   |
| Backend (Node.js)      | 22,000        | Auth, APIs, streaming logic, payment integration    |
| Admin & CMS            | 8,000         | Dashboard, content management                        |
| Shared / config / tests| 7,000         | Utilities, config, test code                        |
| **Total**              | **55,000**    | **KLOC = 55**                                       |

### Effort and Schedule (Semi-detached)

- **KLOC** = 55  
- **a** = 3.0, **b** = 1.12  
- **c** = 2.5, **d** = 0.35  

**Effort:**

```
E = 3.0 × (55)^1.12 ≈ 3.0 × 88.25 ≈ 265 person-months
```

**Development time:**

```
T = 2.5 × (265)^0.35 ≈ 2.5 × 6.93 ≈ 17.3 months
```

**Average team size:**

```
Team size = E / T = 265 / 17.3 ≈ 15 persons
```

### Cost Estimation

Assuming an average cost per person-month (salary + overhead) of **₹1,00,000**:

```
Total cost = E × Cost per person-month = 265 × 1,00,000 = ₹2.65 crores
```

| Item                    | Value              |
|-------------------------|--------------------|
| Effort                  | 265 person-months  |
| Development time        | ~17.3 months       |
| Approx. team size       | ~15 persons        |
| Estimated cost (₹1L/PM) | ₹2.65 crores       |

*Note: Cost per person-month should be adjusted to your organization (location, role mix, overhead).*
