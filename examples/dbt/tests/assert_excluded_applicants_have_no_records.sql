-- Re-counts the set that stg_sis__students excludes. The exclusion was justified by a count of
-- zero; this checks the count is still zero.
--
-- severity = warn: a new row here is not a broken build, it is a question for a person. Someone
-- has to read the warning and decide whether the exclusion is still right (DECISIONS.md
-- 2026-02-17).
--
-- Each returned row is an excluded applicant who now has attendance records.

{{ config(severity = 'warn') }}

with students as (

    select * from {{ source('sis', 'students') }}

),

attendance as (

    select * from {{ source('sis', 'attendance') }}

),

excluded as (

    select cast(student_id as string) as student_id
    from students
    where enrollment_status = 'applicant_placeholder'

),

excluded_with_records as (

    select distinct excluded.student_id
    from excluded
    inner join attendance
        on cast(attendance.student_id as string) = excluded.student_id

)

select * from excluded_with_records
