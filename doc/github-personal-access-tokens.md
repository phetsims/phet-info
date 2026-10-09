# GitHub Personal Access Tokens

If a GitHub Personal Access Token (PAT) has expired or is no longer valid, follow these steps:

* Sign in to https://github.com/settings/profile using phet-dev account
* You will need 2FA from your phet-secure email.
* Generate a new classic token at https://github.com/settings/tokens/new
* Give the token to the process that needs it, this could mean:
  * paste into a build-local.json
  * authenticate by doing an action that needs the token, such as `git pull` on a private repo

To add phet-secure@colorado.edu as a shared secondary account, use these OIT instructions (similar procedures can be 
followed on the desktop app, but there aren’t published instructions).

https://oit.colorado.edu/tutorial/outlook-web-add-shared-email-folder-or-mailbox