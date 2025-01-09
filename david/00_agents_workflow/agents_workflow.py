
import os
import sys

# 获取项目根目录的绝对路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
print(f"system path 目录是：{sys.path}")

print(sys.executable)
from autogen.agentchat.contrib.agent_builder import AgentBuilder
from autogen.oai.openai_utils import config_list_from_json
import autogen
print(autogen.__file__)


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
oai_config_path = os.path.join(parent_dir, "OAI_CONFIG_LIST")
if os.path.exists(oai_config_path):
    # 当使用相对路径时，应该先获取当前os的workspace
    print('当前工作目录是：' + os.getcwd())
    config_list = config_list_from_json(env_or_file=oai_config_path)
else:
    print(f"文件 '{oai_config_path}' 不存在")
    
def start_task(execution_task: str, agent_list: list, llm_config: dict):

    def state_transition(last_speaker, groupchat):
       return groupchat.agents[-1]

    group_chat = autogen.GroupChat(agents=agent_list, 
                                   messages=[], 
                                   max_round=6, 
                                   allow_repeat_speaker = False 
                                   )
    manager = autogen.GroupChatManager(
        groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}
    )
    rst = agent_list[0].initiate_chat(manager, message=execution_task)
    pass

def ask_ossinsight(question: str) -> str:
    return "The repository microsoft/autogen has 123,456 stars on GitHub."

def get_user_emailaddress(user: str) -> str:
    return "xx@qq.com"

def send_email(address: str) -> str:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header

    # QQ邮箱SMTP服务器地址
    smtp_server = "smtp.qq.com"
    smtp_port = 465  # 使用SSL加密

    # 登录信息
    sender_email = "your_email@qq.com"  # 替换为你的QQ邮箱
    auth_code = "your_auth_code"  # 替换为SMTP授权码

    # 收件人
    recipient_email = "recipient_email@example.com"  # 替换为收件人邮箱

    # 创建邮件内容
    subject = "测试邮件"  # 邮件主题
    content = "这是一封由Python发送的测试邮件。"  # 邮件正文

    # 创建MIMEMultipart对象
    message = MIMEMultipart()
    message["From"] = Header("Python邮件测试", "utf-8")
    message["To"] = Header("收件人", "utf-8")
    message["Subject"] = Header(subject, "utf-8")

    # 邮件正文
    message.attach(MIMEText(content, "plain", "utf-8"))

    try:
        # 连接到SMTP服务器并发送邮件
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, auth_code)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败：{e}")

    return "发送成功."

def do_task1():
    task = "给我算下1累加到50的结果，并保存到文件中"
    agent_builder = AgentBuilder(
        config_file_location='F:\\GitHub\\david-autogen\\test2',
        builder_model="gpt-3.5-turbo",
        agent_model="gpt-3.5-turbo",
    )

    # agent_builder.clear_all_agents()

    saved_agents_config_path = f"{script_dir}/task1.json"
    if os.path.exists(saved_agents_config_path):
        agent_list, agent_configs = agent_builder.load(filepath=saved_agents_config_path)
    else:
        workspace = f"{parent_dir}/workspace" 
        agent_list, agent_configs = agent_builder.build(
            building_task=task,
            default_llm_config={"temperature": 0},
            code_execution_config={
                "last_n_messages": 2,
                "work_dir": workspace,
                "timeout": 60,
                "use_docker": "python:3",
            }
        ) 
        agent_builder.save(saved_agents_config_path)

    start_task(
        execution_task=task,
        agent_list=agent_list,
        llm_config={}
    )
    pass

def do_task2():

    def ask_ossinsight(question: str) -> str:
        return "The repository microsoft/autogen has 123,456 stars on GitHub."

    def get_user_emailaddress(user: str) -> str:
        return "xx@qq.com"

    def send_email(address: str) -> str:
        return ''

    list_of_functions = [
        {
            "name": "ossinsight_data_api",
            "description": "This is an API endpoint allowing users (analysts) to input question about GitHub in text format to retrieve the related and structured data.",
            "function": ask_ossinsight,
        },
        {
            "name": "send_email",
            "description": "send email to user",
            "function": send_email,
        },
        {
            "name": "get_user_emailaddress",
            "description": "获取用户的email地址",
            "function": get_user_emailaddress,
        }      
    ]

    task = "给我算下1累加到50的结果，并发送到david的邮箱中"
    agent_builder = AgentBuilder(
        config_file_location='F:\\GitHub\\david-autogen\\test2',
        builder_model="gpt-3.5-turbo",
        agent_model="gpt-3.5-turbo",
    )

    saved_agents_config_path = f"{script_dir}/task2.json"
    if os.path.exists(saved_agents_config_path):
        agent_list, agent_configs = agent_builder.load(filepath=saved_agents_config_path)
    else:
        workspace = f"{parent_dir}/workspace" 
        agent_list, agent_configs = agent_builder.build(
            building_task=task,
            default_llm_config={"temperature": 0},
            code_execution_config={
                "last_n_messages": 2,
                "work_dir": workspace,
                "timeout": 60,
                "use_docker": "python:3",
            },
            list_of_functions=list_of_functions
        ) 
        agent_builder.save(saved_agents_config_path)

    start_task(
        execution_task=task,
        agent_list=agent_list,
        llm_config={}
    )
    pass

if __name__ == "__main__":

    os.environ['AUTOGEN_USE_DOCKER'] = 'False'
    os.environ['OAI_CONFIG_LIST'] = oai_config_path

   # do_task1()
    do_task2()
    pass