# User Role Requirements

## Admin
Admins configure the complete environment.

Permissions:
- Set up community environment and organization structure.
- Add, connect, and configure datapoints.
- Define datapoint meaning, names, units, media, and site assignment.
- Configure actors and control capabilities.
- Configure automations and schedules.
- Import historic readings from CSV.
- Configure energy consultant assignments.
- Add users, delete users, and change roles.
- Manage authentication and integration settings.
- Manage API clients, API tokens, or other machine credentials.
- Manage community personalization settings, including the community logo.

## Community
Community users are clerks or public officials and may not be technically experienced. Their interface must be clean and limited to common workflows.

Permissions:
- Check readings and ratings.
- View current and historic usage.
- Execute allowed automations.
- Adjust allowed timetables or schedules.
- Request reports.
- Download released reports.
- Mark readings as anomalous and request consultant review.
- No direct datapoint creation or low-level system setup.

Fine-grained clerk permissions are a v2 requirement:
- Admins should be able to create clerk/community users whose access is limited to specific villages, sites, objects, actors, or action categories.
- Example: a clerk may be allowed to read values for one gym and control only that gym.
- Control permissions must distinguish at least direct actor commands, temporary overwrites, and timetable/schedule editing.
- The UI should hide unavailable actions, but the backend must enforce the permission scope.

## Community Admin
Community Admins are technically capable municipal users.

Permissions:
- Most Admin-like configuration except adding new datapoints.
- Rename datapoints and reorganize them.
- Configure automations and schedules.
- Import historic readings from CSV.
- Add users, delete users, and change roles where allowed by policy.
- No creation of new physical datapoints unless explicitly granted later.

## Energy Consultant
Energy Consultants provide expert review and report content.

Permissions:
- Set energy estimates for readings and datapoints.
- Define benchmark or target values used for ratings.
- View consultant requests and anomalous readings.
- Add findings and recommendations to requested reports.
- Approve and release reports to become downloadable.
- Recommend saving measures and prioritize follow-up analysis.

## Guest/Public
Guest/Public access must not require login.

Permissions:
- View public overview of readings selected for publication.
- Download reports marked open to the public.
- See aggregated/summarized public report data by default; site-level report details are hidden unless explicitly marked public.
- No control operations.
- No private detail data.
- No user, datapoint, report editing, or anomaly workflow access.

## Cross-Cutting Role Requirements
- All privileged actions must be auditable.
- Control actions must show actor, user, requested state, timestamp, result, and failure reason.
- Role boundaries must be enforced in the backend, not only in the frontend.
- Fine-grained v2 clerk permission checks must be enforced in the backend, including object scope and action type.
- UI navigation must hide unavailable actions but backend authorization remains mandatory.
