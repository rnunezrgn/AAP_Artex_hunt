# AAP 2.6 integration guide

## Suggested project layout

Use this repository as an AAP Project. Publish the collection archive to Private Automation Hub and install it into an Execution Environment.

## Execution Environment

Pin tested versions of:
- `redhat_security.artex_detection`
- `ansible.windows`
- `kubernetes.core`
- `azure.azcollection`

Include Python dependencies required by `kubernetes.core` and `azure.azcollection` in the EE image. Build and test the EE in CI before importing it into AAP.

## Job Templates

Create one Job Template per platform rather than one highly privileged cross-platform template:

| Template | Inventory | Credential | Extra vars |
|---|---|---|---|
| ARTEX - Linux | `linux` | SSH machine credential | `artex_platform: linux` |
| ARTEX - Windows | `windows` | WinRM machine credential | `artex_platform: windows` |
| ARTEX - Kubernetes | `kubernetes_api` | Kubernetes credential/context | `artex_platform: kubernetes` |
| ARTEX - Azure audit | `azure_audit` | No cloud credential needed for offline JSON input | `artex_platform: azure` |

For Kubernetes, grant read-only RBAC for pods in only the namespaces in scope. Avoid cluster-admin. For Azure, obtain audit records through your approved logging pipeline, sanitize them, and provide them as a protected survey/file input. Never pass client secrets, access tokens, or full credential objects as extra vars.

## Workflow

Recommended AAP Workflow Job Template:
1. Linux hunt
2. Windows hunt
3. Kubernetes hunt
4. Azure audit hunt
5. Consolidate findings / notify SOC
6. Human review

Do not automatically isolate or remediate based solely on these findings. The collection is intentionally read-only.

## Results

Each host publishes `artex_scan_summary`. For a production implementation, add an approved result-export task (for example, to an internal SIEM or case-management API) and ensure that credentials are stored in AAP Credentials, not in playbooks or inventories.
