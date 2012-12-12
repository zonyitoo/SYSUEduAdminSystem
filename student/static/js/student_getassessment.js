//JavaScript Document

$(document).ready(function(){
    getAssessment();
    $("#view-assessment-btn").click(function(){
        getAssessment();
    });
});

function getAssessment()
{
    var type_map = new Array();
    type_map[1] = 0;
    type_map[2] = 1;
    type_map[3] = 2;
    type_map[4] = 3;
    var title_dict = new Array(
                new Array(),
                new Array(),
                new Array(
                    "123",
                    "456"
                    ),
                new Array(
                    "教学态度",
                    "教学内容",
                    "教学方法",
                    "教学效果"
                    )
                );
    var subject_dict = new Array(
                new Array(),
                new Array(),
                new Array(
                    new Array(
                        "ABC"
                        ),
                    new Array(
                        "DEF"
                        )
                    ),
                new Array(
                    new Array(
                        "教书育人，为人师表。",
                        "实验教学准备充分，讲课流利。",
                        "批改实验报告及时、认真，辅导耐心。"
                        ),
                    new Array(
                        "熟悉实验内容和仪器使用，指导材料齐备。",
                        "内容设计合理、讲解清晰，示范准确、规范。",
                        "能安排一定的综合性、设计性的实验内容，并将科研成果引入教学。"
                        ),
                    new Array(
                        "教学组织手段灵活有效、教学秩序好。",
                        "善于引导学生运用所学知识分析实验的现象和结果。",
                        "善于启发学生思考，注重师生互动。"
                        ),
                    new Array(
                        "有助于培养学生的创新意识和创新思维。",
                        "有助于提高学生的实验动手能力",
                        "有助于学生巩固相关的理论知识。"
                        )
                    )
                );
    $.ajax({
        url: '/take/getTakeAssessment/',
        type: 'get',
        async: false,
        error: function(jqXHR,textStatus,errorThrown)
        {
            switch(jqXHR.status)
            {
                case 400:
                    alert("网络状态异常，请刷新后重试");
                    break;
                case 401:
                    alert("当前用户已过期，请重新登录");
                    window.location = '/user/login/';
                    break;
                case 403:
                    alert("页面无法访问，请刷新后重试");
                    break;
                case 404:
                    alert("页面不存在，请刷新后重试");
                    break;
                case 500:
                    alert("服务器傲娇");
                    break;
                default:
                    alert(jqXHR.status + "\n" + textStatus + "\n" + errorThrown);
                    break;
            }
        },
        success: function(msg,textStatus,jqXHR)
        {
            var assessment = msg.assessment;
            var course_name,course_type,credit,teacher,filter;
            $("#assessment-result").empty();
            if (assessment.length == 0)
                $("#assessment-result").append("<center>未到教学评分时间或已完成所有教学评分项目</center>");
            else
            {
                $("#assessment-result").append("<div class='accordion'><div id='assessment-list'></div></div>");
                for (var i = 0;i < assessment.length;i++)
                {
                    course_name = assessment[i].course.name;
                    course_type = assessment[i].course.course_type;
                    department = assessment[i].course.department.name;
                    assessment_type = assessment[i].course.assessment_type;
                    credit = assessment[i].course.credit;
                    teacher = assessment[i].course.teacher;
                    filter = type_map[assessment_type];
                    $("#assessment-list").append("<div class='well accordion-group'><div class='accordion-heading' class='accordion-toggle' data-parent='#assessment-list' data-toggle='collapse' href='#assessment-" + i + "'><div id='department-" + i + "' class='hide'>" + department + "</div><div id='course-name-" + i + "' class='hide'>" + course_name + "</div><div>课程名称：" + course_name + "<br>类别：" + course_type + "<br>学分：" + credit + "<br>任课教师：" + teacher.teacher_name + "</div></div><div id='assessment-" + i + "' class='accordion-body collapse'><div id = 'assessment-in-" + i + "' class='accordion-inner'></div></div></div>");
                    var current_block = $("#assessment-in-" + i);
                    for (var j = 0;j < title_dict[filter].length;j++)
                    {
                        current_block.append("<p><strong>" + title_dict[filter][j] + "</strong></p><div id='assessment-" + j + "-" + i + "'></div>");
                        for (var k = 0;k < subject_dict[filter][j].length;k++)
                        {
                            $("#assessment-" + j + "-" + i).append(subject_dict[filter][j][k] + "<br><span id='rate-" + i + "-" + j + "-" + k + "' class='rate " + i + "'></span>&nbsp&nbsp&nbsp<span id='hint-" + i + "-" + j + "-" + k + "' class='hint " + i + "'></span>");
                            $("#rate-" + i + "-" + j + "-" + k).raty({
                                hints: ['1','2','3','4','5'],
                                scoreName: "score",
                                size: 24,
                                starOff: 'star-off-big.png',
                                starOn: 'star-on-big.png',
                                target: '#hint-' + i + '-' + j + '-' + k,
                                targetFormat: '{score}',
                                targetKeep: true,
                            });
                        }
                        current_block.append("<br>");
                    }
                    current_block.append("<br><div id='msg-area-" + i + "' class='hide alert alert-danger'></div><div class='control-group'><div class='controls'><button id='assessment-submit-" + i + "' class='btn btn-primary " + i + "' onclick='sendAssessment(" + i + ");'>提交</button></div></div>");
                }
            }
        }
    });
}

function sendAssessment(index)
{
    var assessment_string = "";
    var flag = true;
    $("." + index + ".hint").each(function(){
        if ($(this).text() == "" || $(this).text() == null)
            flag = false;
        assessment_string += $(this).text() + ",";
    });
    assessment_string = assessment_string.substr(0,assessment_string.length - 1);
    if (flag == false)
    {
        $("#msg-area-" + index).text("请对所有项目都进行评分后再提交");
        $("#msg-area-" + index).show();
        return 0;
    }
    else
    {
        var submit_name = $("#course-name-" + index).text();
        var submit_department = $("#department-" + index).text();
        $.ajax({
            url: '/assessment/submitCourseAssessments/',
            data: 'department=' + submit_department + '&course_name=' + submit_name + '&score=' + assessment_string,
            type: 'post',
            async: false,
            error: function(jqXHR,textStatus,errorThrown)
            {
                switch(jqXHR.status)
                {
                    case 400:
                        alert("网络状态异常，请刷新后重试");
                        break;
                    case 401:
                        alert("当前用户已过期，请重新登录");
                        window.location = '/user/login/';
                        break;
                    case 403:
                        alert("页面无法访问，请刷新后重试");
                        break;
                    case 404:
                        alert("页面不存在，请刷新后重试");
                        break;
                    case 500:
                        alert("服务器傲娇");
                        break;
                    default:
                        alert(jqXHR.status + "\n" + textStatus + "\n" + errorThrown);
                        break;
                }
            },
            success: function(msg,textStatus,jqXHR)
            {
                getAssessment();
            }
        });
    }
}
