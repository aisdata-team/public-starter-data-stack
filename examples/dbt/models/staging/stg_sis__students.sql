-- One row per enrolled student from the student information system.
--
-- Rules applied here (AGENTS.md, "Writing SQL"):
--   * Every id is cast to text, so a later join never compares a number with text and silently
--     drops rows.
--   * Staging renames and casts. Business logic belongs in later models.
--   * Names stay in staging. Reporting tables never carry them; a test enforces that.

with source as (

    select * from {{ source('sis', 'students') }}

),

renamed as (

    select
        cast(student_id as string)   as student_id,
        cast(household_id as string) as household_id,
        cast(grade_level as int64)   as grade_level,
        enrollment_status,
        cast(entry_date as date)     as entry_date,
        first_name,
        last_name
    from source

    -- Placeholder records the SIS creates for applicants who never enrolled. When this was written
    -- none of them had any attendance records (counted 2026-02-17). That is a fact about that day's
    -- data, not a law, so a test re-counts it every night (DECISIONS.md 2026-02-17).
    -- measured-exclusion: counted-by assert_excluded_applicants_have_no_records
    where enrollment_status != 'applicant_placeholder'

)

select * from renamed
