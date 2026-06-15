# Local Operator Run Artifacts

`operator_package_v*` directories are local generated outputs, not source
artifacts for the public repository.

They are ignored because the generated run chain can include internal
owner-review state and deeply nested paths that are not portable for default
Windows checkouts. Keep the source scripts, specs, product app, and concise
quality reports in git; regenerate local run artifacts only inside a private
workspace when they are needed for owner review.
