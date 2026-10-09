# Publish

* [Publish](overview.md) - APIs for making views public, managing private URLs, and updating publish configurations.

# Concepts

* [Create Private URL](create-private-url.md) - Creates a Private URL for a view — generating the secret private key if one does not exist — and, in the same call, sets the link's permission set, row-level filter criteria, column restrictions, password, and expiry date.
* [Get Private URL](get-private-url.md) - Returns the existing Private URL of a view — the open-view URL with the view's secret 32-character private key appended.
* [Get Publish Configurations](get-publish-configurations.md) - Returns the complete publish state of a view in one call: the public channel's audience and listing state, the private channel's password/expiry state, and the presentation configuration used to render the published page.
* [Make View Public](make-views-public.md) - Publishes a view as a Public URL and, in the same call, defines the read-only permission set, the row-level filter criteria, and the column restrictions that apply to public visitors.
* [Remove Private Access](remove-private-access.md) - Removes the view's Private URL entirely — the private key, the associated permission set, the password, and the expiry date.
* [Remove Public Permission](remove-public-permission.md) - Un-publishes the view's Public URL, revoking access for all public visitors.
* [Update Publish Configurations](update-publish-configurations.md) - Updates the presentation configuration of the view's published page — title, description, toolbar, search box, dimensions, auto-refresh interval, legend position, URL-level criteria, Ask Zia — and, when the workspace is public, its public-listing flag.
