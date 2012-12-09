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
    type_map["公选"] = 0;
    type_map["公必"] = 1;
    type_map["专选"] = 2;
    type_map["专必"] = 3;
    var title_dict = new Array(new Array(),new Array(),new Array("教学态度","教学内容","教学方法","教学效果"),new Array());
    var subject_dict = new Array(new Array(),new Array(),new Array(new Array("教书育人，为人师表。","实验教学准备充分，讲课流利。","批改实验报告及时、认真，辅导耐心。"),new Array("熟悉实验内容和仪器使用，指导材料齐备。","内容设计合理、讲解清晰，示范准确、规范。","能安排一定的综合性、设计性的实验内容，并将科研成果引入教学。"),new Array("教学组织手段灵活有效、教学秩序好。","善于引导学生运用所学知识分析实验的现象和结果。","善于启发学生思考，注重师生互动。"),new Array("有助于培养学生的创新意识和创新思维。","有助于提高学生的实验动手能力","有助于学生巩固相关的理论知识。")),new Array());
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
            $("#assessment-result").empty();
            $("#assessment-result").append("<table class='accordion table table-bordered table-hover table-condensed'><thead><tr><th class='very-wide-block'>课程名称</th><th class='narrow-block'>类别</th><th class='narrow-block'>学分</th><th class='narrow-block'>任课教师</th><th class='very-wide-block'>教学评分</th></tr></thead><tbody id='assessment-list'></tbody></table>");
            var assessment = msg.assessment;
            var course_name,course_type,credit,teacher,filter;
            for (var i = 0;i < assessment.length;i++)
            {
                course_name = assessment[i].course.name;
                course_type = assessment[i].course.course_type;
                credit = assessment[i].course.credit;
                teacher = assessment[i].course.teacher;
                filter = type_map[course_type];
                $("#assessment-list").append("<tr><td>" + course_name + "</td><td>" + course_type + "</td><td>" + credit + "</td><td>" + teacher.teacher_name + "</td><td id='assessment-" + i + "'></td></tr>");
                var assessment_block = $("#assessment-" + i);
                for (var j = 0;j < title_dict[filter].length;j++)
                {
                    assessment_block.append("<div class='accordion-group'><div class='accordion-heading'><div class='accordion-toggle' data-toggle='collapse' data-parent='#assessment-" + i + "' data-target='#assessment-" + j + "-" + i + "'><strong>" + title_dict[filter][j] + "</strong></div></div><div id='assessment-" + j + "-" + i + "' class='accordion-body collapse'><div class='accordion-inner " + j + "' style='text-align: left;'></div></div></div>");
                    for (var k = 0;k < subject_dict[filter][j].length;k++)
                        $("." + j + ".accordion-inner").append(subject_dict[filter][j][k] + "<div class='rate'></div>");
                }
                $(".rate").raty({
                    hints: ['1','2','3','4','5'],
                    scoreName: "score"
                });
            }
        }
    });
}
