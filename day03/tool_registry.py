from day03.tools import search_job_tool,city_average_salary_tool

search_job_schema = {
    "type":"object",
    "properties":{
        "city":{"type":"string"},
        "min_salary":{
            "type":"integer",
            "description":"最低薪资，必须直接使用用户输入的整数，不进行单位换算。"
            "例如用户输入160，则返回160。"
            },
        "keyword":{"type":"string"}
    },
       "required":[
        "city",
        "min_salary",
        "keyword"
    ]
}


city_average_salary_schema = {
    "type":"object",
    "properties":{
        "city":{
            "type":"string",
            "description":"要查询平均薪资的城市名字"
        },
    },
        "required":[
            "city"
        ]
}


tool_definitions = [
    {
        "type":"function",
        "function":{
            "name":"search_job_tool",
            "description":"根据城市、最低薪资和岗位关键词查询符合条件的岗位",
            "parameters":search_job_schema
        }
    },
        {
            "type":"function",
            "function":{
                "name":"city_average_salary_tool",
                "description":"查询指定城市岗位的平均薪资",
                "parameters":city_average_salary_schema
            }
        }
]

tool_map = {
    "search_job_tool":search_job_tool,
    "city_average_salary_tool":city_average_salary_tool
}