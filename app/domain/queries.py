class Queries:
    @staticmethod
    def deps_over_mean_query():
        query = """
            WITH count_2021 AS (
              SELECT
                department,
                count(name) AS cnt
              FROM
                `cwp-project-272117.sandbox.hired_employees`
              WHERE department IS NOT NULL
              AND job IS NOT NULL
              AND name IS NOT NULL
              AND `datetime` BETWEEN '2021-01-01' AND '2021-12-31' 
              GROUP BY 1
            ),
            mean_2021 AS (
              SELECT 
                avg(cnt) as mean
              FROM count_2021
            ),
            departments_count AS (
              SELECT
                department,
                count(name) AS cnt
              FROM
                `cwp-project-272117.sandbox.hired_employees`
              WHERE department IS NOT NULL
              AND job IS NOT NULL
              AND name IS NOT NULL
              GROUP BY 1
            ),
            departments AS (
              SELECT
                id,
                department
              FROM
                `cwp-project-272117.sandbox.departments`
              WHERE department IS NOT NULL
            )
            SELECT 
              CAST(dc.department AS INT) AS id,
              d.department,
              dc.cnt AS hired
            FROM departments_count dc
            JOIN mean_2021 m
            ON dc.cnt > m.mean
            JOIN departments d
            ON dc.department = d.id
            ORDER BY hired DESC
            """

        return query

    @staticmethod
    def hires_by_quarter_query():
        query = """
            SELECT 
              d.department, 
              j.job,
              SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
              SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
              SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
              SUM(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
            FROM `cwp-project-272117.sandbox.hired_employees` h
            JOIN `cwp-project-272117.sandbox.departments` d
            ON h.department_id = d.id
            JOIN `cwp-project-272117.sandbox.jobs` j
            ON h.job_id = j.id
            WHERE h.department_id IS NOT NULL 
              AND h.job_id IS NOT NULL 
              AND h.name IS NOT NULL
              AND EXTRACT(YEAR FROM `datetime`) = 2021
            GROUP BY 1,2
            ORDER BY 1,2
            """

        return query
