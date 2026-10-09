# Asynchronous & Batch Data Import

* [Asynchronous & Batch Data Import](overview.md) - APIs for creating and monitoring asynchronous import jobs and batch imports.

# Concepts

* [Batch Import Data into Existing Table](batch-import-existing-table.md) - Loads an existing table from several uploads belonging to one import job.
* [Batch Import Data into New Table](batch-import-new-table.md) - Creates a new table and loads it from several uploads, all belonging to one import job.
* [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md) - Uploads a file and loads it into an existing table in the background, appending, replacing, or merging according to importType.
* [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md) - Uploads a file, creates a new table from it, and returns a job ID for tracking.
* [Get Import Job Details](get-import-job-details.md) - Returns the current state of an import job and, once it has finished, the full import summary.
