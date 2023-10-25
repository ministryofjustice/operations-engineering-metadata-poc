# Web Application Security Assessment

## Context

The web application is publicly accessible on the internet, making it susceptible to various security threats.
Understanding these threats and their potential impact on Confidentiality, Integrity, and Availability (CIA) is crucial
for ensuring the application's security posture.

This assessment will be carried out in the context of current mitigations and as they apply to a PoC/Testing
Environment.

## Current Vulnerabilities

### API Endpoint POST /api/user/add

#### Impact: `LOW`

#### Description

The API endpoint `POST /api/user/add` currently is available via the public internet. The endpoint currently
validates the input by checking the `github_username` provided, against a static allow list. If allowed, the system will
attempt to persist the data in an RDS database instance.

An attacker could attempt to spam the endpoint and send multiple requests using the publicly available static allow list
of `github_username`'s - attempting to increase the cost of the system through increasing the cost of data persistence.

The schema of the database ensures only a single record can be created with the `github_username` - therefor, attempts
to store multiple records would be rejected at the database level. Ideally, security measures in prior layers should
mitigate this issue.

#### CIA Assessment (in the context of PoC/Testing Environment)

- **Confidentiality**: `Low` - An attacker would not be able to gain access to any sensitive information through this
  attack, since the endpoint only returns the data provided to it.
- **Integrity**: `Low` - An attacker could populate the initial data of the allow list in the database via this attack.
  Although this data is not being consumed by any services
- **Availability**: `Low` - An attacker could continuously raise these requests to overload the pod and database. With
  it being a testing environment, it's availability is not essential to any of MoJs processes or services.

#### Rationale

For this endpoint, security measures are in place to mitigate exploitation of persistent storage in RDS, via a static
allow list.

This enables the endpoint to run in a PoC/Testing Environment.

Although, when deploying to a production environment, ensure
reasonable mitigations are in place for the service to securely run in a production environment.

The current mitigations are not enough to enable a production service. Attackers ideally should not be able to initiate
a connection to a production database contaminating potentially sensitive information

### API Endpoint GET /api/user/\*\*

#### Impact: `LOW`

#### Description

The API endpoints `GET /api/user/**` are currently available via the public internet. The endpoints currently take data
provided in the URL and use this to query the database for a match on the key/value pair i.e.
calling `GET /api/user/email/test@example.com` will execute a `SELECT` SQL Query on the `users` table to for the first
match where
the `email` column equals `test@example.com`.

#### CIA Assessment (in the context of PoC/Testing Environment)

- **Confidentiality**: `Low` - All data in the database is available to be queried. Although allow lists have been
  implemented for populating this data, which means only test and pre-approved data can be populated in the database,
  and
  therefor retrieved from the database.
- **Integrity**: `Low` - There is no impact on integrity.
- **Availability**: `Low` - This system is isolated from any production services and resources, therefor no impact on
  availability.

#### Rationale

For this endpoint, attackers could easily affect the availability of the system through a DDoS attack. With this being a
testing environment, this is of little to no risk.

However, in terms of confidentiality, this endpoint does depend on a temporary allow list existing in the `POST`
endpoint. Although this is suitable for a testing environment, further layers of security will be needed in a production
environment - such as a proper authentication/authorisation flow.

## Decision

The system, as is, is suitable to run in a testing environment for the current functionality - given that the current
security mitigations are in place.

This is due to the mitigations minimising the risk of data confidentiality through static allow lists defined in code.

It's worth noting that the current mitigations are not suitable for a production environment. When the system is ready
to be deployed into a production environment, the team will re-assess the system to determine whether it's suitable for
the production environment.
