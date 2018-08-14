# 基于python3.6镜像来构建owllook镜像
FROM python:3.6
MAINTAINER howie6879 <howie6879@gmail.com>
RUN apt update -y && apt-get install -y net-tools
# 设置环境变量
ENV APP_ROOT /opt
WORKDIR ${APP_ROOT}/
COPY Pipfile ${APP_ROOT}/
COPY Pipfile.lock ${APP_ROOT}/
# 安装依赖
RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ pipenv
RUN pipenv install
ENV TIME_ZONE=Asia/Shanghai
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
COPY . ${APP_ROOT}
WORKDIR ${APP_ROOT}/owllook/
RUN find . -name "*.pyc" -delete
# 启动
CMD ["pipenv","run","python","run.py"]