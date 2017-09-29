```
~/dev/etc/ecip1017test dev *% ⟠ ./bin/deploy.sh etc-tester us-central1-a ecip1017test
Updated property [core/project].
Updated property [compute/zone].
Updated property [container/cluster].
ERROR: (gcloud.container.clusters.get-credentials) You do not currently have an active account selected.
Please run:

  $ gcloud auth login

to obtain new credentials, or if you have already logged in with a
different account:

  $ gcloud config set account ACCOUNT

to select an already authenticated account to use.
~/dev/etc/ecip1017test dev *% ⟠ gcloud auth login
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?redirect_uri=http%3A%2F%2Flocalhost%3A8085%2F&prompt=select_account&response_type=code&client_id=32555940559.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fappengine.admin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faccounts.reauth&access_type=offline


WARNING: `gcloud auth login` no longer writes application default credentials.
If you need to use ADC, see:
  gcloud auth application-default --help

You are now logged in as [isaac.ardis@gmail.com].
Your current project is [etc-tester].  You can change this setting by running:
  $ gcloud config set project PROJECT_ID
~/dev/etc/ecip1017test dev *% ⟠ ./bin/deploy.sh etc-tester us-central1-a ecip1017test
Updated property [core/project].
Updated property [compute/zone].
Updated property [container/cluster].
WARNING: Accessing a Container Engine cluster requires the kubernetes commandline
client [kubectl]. To install, run
  $ gcloud components install kubectl

Fetching cluster endpoint and auth data.
kubeconfig entry generated for ecip1017test.
./bin/deploy.sh: line 14: kubectl: command not found
~/dev/etc/ecip1017test dev *% ⟠ gcloud components install kubectl


Your current Cloud SDK version is: 172.0.1
Installing components from version: 172.0.1

┌──────────────────────────────────────────────────────────────────┐
│               These components will be installed.                │
├─────────────────────┬─────────────────────┬──────────────────────┤
│         Name        │       Version       │         Size         │
├─────────────────────┼─────────────────────┼──────────────────────┤
│ kubectl             │                     │                      │
│ kubectl             │               1.7.5 │             15.9 MiB │
└─────────────────────┴─────────────────────┴──────────────────────┘

For the latest full release notes, please visit:
  https://cloud.google.com/sdk/release_notes

Do you want to continue (Y/n)?  Y

╔════════════════════════════════════════════════════════════╗
╠═ Creating update staging area                             ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: kubectl                                      ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: kubectl                                      ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Creating backup and activating new installation          ═╣
╚════════════════════════════════════════════════════════════╝

Performing post processing steps...done.

Update done!

WARNING:   There are older versions of Google Cloud Platform tools on your system PATH.
  Please remove the following to avoid accidentally invoking these old tools:

  /usr/local/Cellar/app-engine-go-64/1.9.48/share/app-engine-go-64/dev_appserver.py


~/dev/etc/ecip1017test dev *% ⟠ ./bin/deploy.sh etc-tester us-central1-a ecip1017test
Updated property [core/project].
Updated property [compute/zone].
Updated property [container/cluster].
Fetching cluster endpoint and auth data.
kubeconfig entry generated for ecip1017test.
service "gm1" created
service "gm2" created
service "g1" created
service "g2" created
service "g3" created
service "p1" created
service "p2" created
service "p3" created
replicationcontroller "node-gm1-rc" created
replicationcontroller "node-gm2-rc" created
replicationcontroller "node-g1-rc" created
replicationcontroller "node-g2-rc" created
replicationcontroller "node-g3-rc" created
replicationcontroller "node-p1-rc" created
replicationcontroller "node-p2-rc" created
replicationcontroller "node-p3-rc" created
Please give 2-3 minutes to spin up nodes before calling bin/status.py
```