# Security And Authentication Requirements

## Login
- Users must be able to log in.
- Authentication must follow current best practices.
- German and English UI text must be supported for authentication flows.

## MFA / 2FA
At least these second-factor options should be supported:
- Authenticator app / TOTP.
- Email-based second factor.

All privileged users must use 2FA. Email-based one-time codes are allowed as a supported 2FA method, alongside authenticator app/TOTP.

## External Identity Providers
The product should support municipal user management integrations:
- OIDC as the preferred modern SSO protocol.
- LDAP / Active Directory for municipalities without OIDC-capable identity infrastructure.
- SAML for customers whose existing SSO requires it.

Approved identity integration priority:
1. OIDC first.
2. LDAP / Active Directory second.
3. SAML third.

Direct local login remains available for initial/demo use and for deployments without an external identity provider.

## Authorization
- Use role-based access control.
- Enforce authorization in the backend.
- Separate public access from authenticated access.
- Scope permissions by organization and potentially by site/building.
- Control actions and administrative changes require audit logging.
- V2 must support fine-grained clerk authorization for municipal users, scoped by village/site, object, actor, and action type where needed.
- Fine-grained control authorization must distinguish reading values, direct actor commands, temporary overwrites, timetable/schedule editing, and administrative setup.
- A user who can temporarily overwrite an actor must not automatically be allowed to edit recurring timetables unless explicitly granted.
- A user who can read an object must not automatically be allowed to control it unless explicitly granted.

## API Credentials
External API security is a required design topic.

Approved production direction:
- Use OAuth 2.0 Client Credentials for external ingestion and actor-control APIs.
- Use scoped, short-lived access tokens.
- Use scopes such as `readings:write`, `readings:read`, `actors:control`, and `reports:read`.
- Scoped API tokens may be acceptable for early demo/development use only.
- Plan mTLS as an optional higher-security mode for actor control, gateways, and sensitive deployments.

Admin UI requirement:
- Admin users need an interface to manage machine/API credentials.
- For the production OAuth2 Client Credentials direction, the UI should manage API clients/integration credentials rather than only raw tokens.
- Admin users must be able to create API clients, assign scopes, assign allowed organization/site/protocol scope once finalized, view metadata, rotate credentials, disable/revoke credentials, and view last-used/audit metadata.
- Client secrets must be shown only once at creation and never shown again.
- For early demo/development scoped API tokens, the same UI can be represented as "API credentials" without implementing full OAuth yet.

Approved external integration scoping:
- User/action-oriented permissions are scoped at the organization level.
- Data-ingestion/query permissions are scoped at the site level.
- Protocol/integration-specific permissions are additionally scoped by protocol or connector type where relevant.
- Datapoint/actor-level scoping remains a future option, but is not the default v1 model.
- Datapoint/actor-level scoping for human clerk users is a v2 product requirement, separate from the v1 external integration scoping model.

## Security-Sensitive Features
- Actor control.
- User and role management.
- API token management.
- Report publication.
- Consultant release decisions.
- CSV imports that can overwrite or distort historic data.

## Audit Requirements
Audit logs should capture:
- user or machine principal;
- action type;
- target object;
- before/after summary where practical;
- timestamp;
- source IP or integration identity;
- success/failure result.
