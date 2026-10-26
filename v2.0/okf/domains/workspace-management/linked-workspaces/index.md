# Linked Workspaces

* [Linked Workspaces](overview.md) - APIs for listing, linking, syncing and unlinking client workspaces against a master workspace, and for checking which workspaces can be linked.

# Concepts

* [Get Linkable Workspaces](get-linkable-workspaces.md) - Returns, grouped by organisation, the workspaces the caller may offer as link candidates for a given master.
* [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md) - Returns, per linked sandbox, what the last sync did entity by entity and what is still waiting to be pushed.
* [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) - Returns the links of a single master workspace, in the same shape as one entry of Get Linked Workspaces For Organization - but as a single object, not an array.
* [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) - Returns every master↔client link in the organisation named by ZANALYTICS-ORGID, grouped one entry per master workspace.
* [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) - Runs the full linking validation against a set of candidate client workspaces without linking anything, and returns a per-workspace verdict with the conflicting entities broken out.
* [Link Workspaces](link-workspaces.md) - Links one or more client workspaces to a master.
* [Sync Linked Workspaces](sync-linked-workspaces.md) - Pushes the master workspace's design to its linked clients.
* [Unlink Workspaces](unlink-workspaces.md) - Removes links between a master workspace and its clients, either all of them or a named set.
