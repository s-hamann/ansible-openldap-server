OpenLDAP Server
===============

This role configures a standalone OpenLDAP server on the target system.

Requirements
------------

If TLS encryption (i.e. LDAPS or LDAP with STARTTLS) is desired, the target system needs to have a suitable X.509 certificate.
Likewise, when client certificates are required of the LDAP clients, the issuing CA's certificate needs to be present on the target system.
This roles does not handle deploying certificates.

If the target system runs Alpine Linux, Ansible must be configured to use Python 3 on the target system.
This is due to Alpine no longer packaging python-ldap for Python 2.

When this role sets passwords for entries with the object class `sambaSamAccount` but no `sambaNTPassword` attribute and `openldap_server_sync_samba` is `false`, the `sambaNTPassword` attribute is automatically set to match the newly set password.
This requires passlib to be available on the controller.
If passlib is not installed, the respective tasks will fail, but not cause the role to fail.

Role Variables
--------------

* `openldap_server_use`  
  A list of USE flags to set (or unset) on `net-nds/openldap`.
  Use flags that are required by this role or the chosen configuration settings are handled automatically and need not be included here.
  Empty by default.
  Only used on Gentoo.
* `openldap_server_overlays`  
  A list of overlays to activate.
  Note: Modules required by these overlays are loaded automatically and need not be configured in `openldap_server_modules`.
* `openldap_server_schemas`  
  A list of schemas to load.
  Entries can either be names (e.g. `core`) or paths to remote files in LDIF format (e.g. `/etc/openldap/schema/core.ldif`).
  The schemas must be present on the remote system or in the `files/schemas` directory of this role.
  Dependencies between schemas are not resolved automatically.
  Note: Schemas required by overlays in `openldap_server_overlays` are automatically added to this list.
  Default is to only load the `core` schema.
* `openldap_server_modules`  
  A list of modules to load.
  Entries are file names and can be absolute or relative to the module directory.
  Note: Overlay modules and backend modules for the databases in use are automatically added to this list.
* `openldap_server_sync_samba`  
  Keep `userPassword` in sync with the fields required by Samba.
  This uses the `smbk5pwd` overlay, which is automatically activated.
  Defaults to `false`.
* `openldap_server_sync_kerberos`  
  Keep `userPassword` in sync with the fields required by Kerberos.
  This uses the `smbk5pwd` overlay, which is automatically activated.
  Defaults to `false`.
* `openldap_server_overlay_config`  
  A dictionary of overlay-specific configurations.
  Keys are overlay names, values are dictionaries containing the configuration for the respective overlay.
  Defaults are taken from `openldap_server_overlay_defaults` (see `defaults/main.yml`).
  Optional.
* `openldap_server_default_root_dn`  
  The default relative DN for the root account.
  The respective tree's DN is appended to this value to generate the full DN.
  Can be overwritten per DIT.
  This is also the root DN in `cn=config`.
  Optional.
* `openldap_server_default_root_password`  
  The default password for the root account.
  Can be overwritten per DIT.
  This is also the password in `cn=config`.
  Optional.
* `openldap_server_skip_default_acls`  
  This role sets up a set of default ACLs that are usually required for correct operation and/or security.
  By setting this variable to `true`, these are not configured.
  Default is `false`.
* `openldap_server_loglevel`  
  A list of OpenLDAP log level names.
  Messages associated with these levels are logged, others are silently ignored.
  Default is only `stats`.
  Other valid values are `trace`, `packets`, `args`, `conns`, `BER`, `filter`, `config`, `ACL`, `stats`, `stats2`, `shell`, `parse`, `cache`, `index`, `sync` and `none`.
  Refer to the OpenLDAP documentation for their meaning.
  Set to `-` to disable all non-critical log messages.
* `openldap_server_sizelimit_soft`  
  The global soft limit on the number of returned results.
  Default is `500`.
* `openldap_server_sizelimit_hard`  
  The global hard limit on the number of returned results.
  Default is the same value as the soft limit.
* `openldap_server_sizelimit_unchecked`  
  The global limit on the number of elements examined by a search.
  Default is unlimited.
* `openldap_server_timelimit_soft`  
  The global soft time limit on queries (in seconds).
  Default is `3600` (1 hour).
* `openldap_server_timelimit_hard`  
  The global hard time limit on queries (in seconds).
  Default is the same value as the soft limit.
* `openldap_server_tls_cert`  
  Path to a PEM-encoded X.509 certificate for slapd to use.
  The file needs to exist and be readable by the OpenLDAP user.
  Default is unset, which disables STARTTLS support.
* `openldap_server_tls_cert_key`  
  Path to the PEM-encoded private key file for the certificate.
  The file needs to exist and be readable by the OpenLDAP user.
  Default is unset.
* `openldap_server_tls_client_ca`  
  Path to a PEM-encoded list of X.509 CA certificates that can sign client certificates.
  The file needs to exist and be readable by the OpenLDAP user.
  Default is unset, which means that no client certificates are requested.
* `openldap_server_tls_enforce_client`  
  When set to `true` (the default), clients must supply a valid certificate.
  When set to `false`, the certificate is optional but must be valid, if supplied.
  This setting has no effect if `openldap_server_tls_client_ca` is not set.
* `openldap_server_tls13_only`  
  Set to `true` to enforce TLSv1.3 only.
  If set to `false` (the default), TLSv1.2 is enforced as the minimal supported protocol version.
* `openldap_server_ciphers`  
  A string describing the ciphers suites that slapd should enable.
  The default depends on whether OpenLDAP was linked against the OpenSSL or GnuTLS library, but in either case contains only strong AEAD cipher suites with PFS.
* `openldap_server_extra_groups`  
  A list of groups that the OpenLDAP system user is added to.
  This allows granting access to additional resources, such as the private key file.
  All groups need to exist on the target system; this role does not create them.
  Empty by default.
* `openldap_server_inaccessible_paths`  
  If the target system uses systemd, this option takes a list of paths, that should not be accessible at all for OpenLDAP.
  Regardless of this option, home directories are made inaccessible and the rest of the file system is mostly read-only.
  Optional.
* `openldap_server_dit`  
  A list of per-DIT configuration setting dictionaries.
  The following keys are valid:
  * `database`  
    The backend database to use. Defaults to `mdb`.
  * `db_directory`
    The path where the database is stored. The default is distribution-dependent.
  * `root_dn`  
    The DN of the root account of the DIT.
    Defaults to `openldap_server_default_root_dn`.
    Set to `omit` to not set a root DN, even if `openldap_server_default_root_dn` is set.
    Optional.
  * `root_password`  
    The password of the root account of the DIT.
    Defaults to `openldap_server_default_root_password`.
    Optional.
  * `ppolicy_dn`  
    The DN containing the default password policy for this DIT (excluding the DIT's base DN).
    Defaults to `cn=default,ou=policies`.
    Ignored if `openldap_server_ppolicy` is `false`.
  * `samba_sid`  
    SID of the Samba domain.
    This is used to generate correct `SambaSID` attributes for entries that need it but do not have it in their `attributes`.
    Optional.
    If unset, it is randomly generated.
  * `indices`  
    A dictionary of indices to set up.
    Dictionary keys are names of attributes to be indexes and values are lists their index types.
    Example: `cn: [eq, sub]`
  * `acls`  
    A list of ACLs to set for this DIT in addition to the default ACLs.
    Each ACL is a string, as described in the OpenLDAP documentation.
    Optional.
  * `db_max_size`  
    Maximal size the DIT may take up.
    Values can be in "human readable" form, e.g. `1 GB` for 1 GiB.
    `100 MB` is the default.
  * `db_checkpoint_bytes`  
    Create a database checkpoint after writing this amount of data.
    Values can be in "human readable" form.
    Defaults to `0`.
  * `db_checkpoint_time`  
    Create a database checkpoint after this time (in minutes).
    Defaults to `0`.
  * `data`  
    A dictionary containing the data to load into the DIT as the root entry.
    The following keys are valid:
    * `dn`
      A list of attribute names that make up the RDN of this entry.
      For the root entry, this defines the base DN (or suffix) of the DIT.
    * `objectClass`
      A string or list of strings to use as the object class of the entry.
    * `attributes`
      A dictionary of attributes to set for the entry.
      Valid key and values are determined by the object classes.
      The attributes listed in `dn` need to be present in this dictionary.
    * `children`  
      A list of entries at the next level.
      Each entry is a dictionary; valid keys are the same as for the `data` element.
      Optional.

Example Configuration
---------------------

The following shows a working example configuration:

```yaml
openldap_server_schema:
  - core
  - cosine
  - rfc2307bis
openldap_server_overlays:
  - memberof
  - ppolicy
openldap_server_overlay_config:
  memberof:
    olcMemberOfGroupOC: 'groupOfMembers'
    olcMemberOfMemberAd: 'member'
    olcMemberOfMemberOfAd: 'memberOf'
openldap_server_sync_samba: true
openldap_server_default_root_dn: 'cn=admin'
openldap_server_dit:
  - indices:
      cn: eq
      objectClass: eq
    acls:
      # PAM
      - 'to dn.one="ou=people,o=example organization" attrs=@posixAccount by group/groupOfMembers/member.exact="cn=posix,ou=groups,o=example organization" read by * break'
      - 'to dn.one="ou=groups,o=example organization" attrs=@posixGroup,@groupOfMembers by group/groupOfMembers/member.exact="cn=posix,ou=groups,o=example organization" read by * break'
      # Samba
      - 'to dn.one="ou=people,o=example organization" attrs=@sambaSamAccount,@posixAccount by group/groupOfMembers/member.exact="cn=samba,ou=groups,o=example organization" read by * break'
      - 'to dn.one="ou=groups,o=example organization" attrs=cn,@sambaGroupMapping by group/groupOfMembers/member.exact="cn=samba,ou=groups,o=example organization" read by * break'
      - 'to dn.exact="sambaDomainName=example domain,o=example organization" attrs=@sambaDomain by group/groupOfMembers/member.exact="cn=samba,ou=groups,o=example organization" read by * break'
    data:
      dn: ['o'] # o=example organization
      objectClass: 'organization'
      attributes:
        o: 'example organization'
      children:
        - dn: ['ou'] # ou=people,o=example organization
          objectClass: 'organizationalUnit'
          attributes:
            ou: 'people'
          children:
            - dn: ['cn']
              objectClass:
                - 'account'
                - 'posixAccount'
                - 'sambaSamAccount'
              attributes:
                cn: 'example user'
                uid: 'example'
                uidNumber: 1000
                gidNumber: 513
                homeDirectory: '/home/example'
                userPassword: 'very secret'
        - dn: ['ou'] # ou=groups,o=example organization
          objectClass: 'organizationalUnit'
          attributes:
            ou: 'groups'
          children:
            - dn: ['cn'] # cn=posix,ou=groups,o=example organization
              objectClass: 'groupOfMembers'
              attributes:
                cn: 'posix'
                description: 'Systems that can access POSIX accounts in LDAP'
            - dn: ['cn'] # cn=samba,ou=groups,o=example organization
              objectClass: 'groupOfMembers'
              attributes:
                cn: 'samba'
                description: 'Systems that can access Samba accounts in LDAP'
            - dn: ['cn'] # cn=Domain Users,ou=groups,o=example organization
              objectClass:
                - 'groupOfMembers'
                - 'posixGroup'
                - 'sambaGroupMapping'
              attributes:
                cn: 'Domain Users'
                sambaSID: '513'
                sambaGroupType: 2
                gidNumber: 513
                description: 'Netbios Domain Users'
                member: 'cn=example user,ou=people,o=example organization'
            - dn: ['cn'] # cn=Users,ou=groups,o=example organization
              objectClass:
                - 'groupOfMembers'
                - 'posixGroup'
                - 'sambaGroupMapping'
              attributes:
                cn: 'Users'
                sambaSID: 'S-1-5-32-545'
                sambaGroupType: 4
                gidNumber: 545
                description: 'Users'
        - dn: ['ou'] # ou=policies,o=example organization
          objectClass: 'organizationalUnit'
          attributes:
            ou: 'policies'
          children:
            - dn: ['cn'] # cn=default,ou=policies,o=example organization
              objectClass:
                - 'device'
                - 'pwdPolicy'
              attributes:
                cn: 'default'
                description: 'default password policy'
                pwdAttribute: 'userPassword'
                pwdCheckQuality: '1'
                pwdMinLength: '8'
                pwdLockout: 'TRUE'
                pwdLockoutDuration: '600'
                pwdMaxFailure: '5'
                pwdFailureCountInterval: '3600'
                pwdMustChange: 'TRUE'
        - dn: ['sambaDomainName'] # sambaDomainName=example domain,o=example organization
          objectClass: 'sambaDomain'
          attributes:
            sambaDomainName: 'example domain'
            sambaPwdHistoryLength: 0
            sambaMinPwdAge: 0
            sambaMaxPwdAge: -1
```


Known Bugs
----------

While LDAP is mostly case insensitive, YAML is not.
This leads issues when attributes or object classes are not cased as expected.
It is recommended always using the exact same camelCase spelling as used in the schema definition files.

License
-------

MIT, except for the following files:
* `samba.ldif` is part of the Samba distribution and licensed under the GNU GPL 3.0.
* `krb5-kdc.ldif` is a conversion of `krb5-kdc.schema`, which is part of the Heimdal project and licensed under the 3-clause BSD license.
