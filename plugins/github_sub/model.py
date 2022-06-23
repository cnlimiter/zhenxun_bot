import re

from services.log import logger
from services.db_context import db
from datetime import datetime
from typing import Optional, List


class GitHubSub(db.Model):
    __tablename__ = "github_sub"

    id = db.Column(db.Integer(), primary_key=True)
    sub_type = db.Column(db.String(), nullable=False)
    # 订阅用户
    sub_users = db.Column(db.String(), nullable=False)
    # 地址
    sub_url = db.Column(db.String())
    update_time = db.Column(db.DateTime())
    # etag
    etag = db.Column(db.String())

    @classmethod
    async def add_github_sub(
            cls,
            sub_type: str,
            sub_user: str,
            *,
            sub_url: Optional[str] = None,
    ) -> bool:
        """
        说明：
            添加订阅
        参数：
            :param sub_type: 订阅类型
            :param sub_user: 订阅此条目的用户
            :param sub_url: 订阅地址
        """
        try:
            async with db.transaction():
                query = (await cls.query.where(cls.sub_url == sub_url).with_for_update().gino.first())
                sub_user = sub_user if sub_user[-1] == "," else f"{sub_user},"
                if query:
                    if sub_user not in query.sub_users:
                        sub_users = query.sub_users + sub_user
                        await query.update(sub_users=sub_users).apply()
                else:
                    sub = await cls.create(
                        sub_url=sub_url, sub_type=sub_type, sub_users=sub_user
                    )
                    await sub.update(
                        sub_url=sub_url if sub_url else sub.sub_url,
                        update_time=datetime.now().replace(microsecond=0)
                    ).apply()
                return True
        except Exception as e:
            logger.info(f"github_sub 添加订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def delete_github_sub(cls, sub_url: str, sub_user: str) -> bool:
        """
        说明：
            删除订阅
        参数：
            :param sub_url: 订阅地址
            :param sub_user: 删除此条目的用户
        """
        try:
            async with db.transaction():
                query = (
                    await cls.query.where(
                        (cls.sub_url == sub_url) & (cls.sub_users.contains(sub_user))
                    )
                        .with_for_update()
                        .gino.first()
                )
                if not query:
                    return False
                strinfo = re.compile(f"\d*:{sub_user},")
                await query.update(
                    sub_users=strinfo.sub('', query.sub_users)).apply()
                if not query.sub_users.strip():
                    await query.delete()
                return True
        except Exception as e:
            logger.info(f"github_sub 删除订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def get_sub(cls, sub_url: str) -> Optional["GitHubSub"]:
        """
        说明：
            获取订阅对象
        参数：
            :param sub_url: 订阅地址
        """
        return await cls.query.where(cls.sub_url == sub_url).gino.first()

    @classmethod
    async def get_sub_data(cls, id_: str) -> List["GitHubSub"]:
        """
        获取 id_ 订阅的所有内容
        :param id_: id
        """
        query = cls.query.where(cls.sub_users.contains(id_))
        return await query.gino.all()

    @classmethod
    async def update_sub_info(
            cls,
            sub_url: Optional[str] = None,
            *,
            update_time: Optional[datetime] = None,
            etag: Optional[str] = None,
    ) -> bool:
        """
        说明：
            更新订阅信息
        参数：
            :param sub_url: 订阅地址
            :update_time: 更新时间
            :etag: 更新标签
        """
        try:
            async with db.transaction():
                sub = (await cls.query.where(cls.sub_url == sub_url).with_for_update().gino.first())
                if sub:
                    await sub.update(
                        update_time=update_time
                        if update_time is not None
                        else sub.update_time,
                        etag=etag
                        if etag is not None
                        else sub.etag
                    ).apply()
                    return True
        except Exception as e:
            logger.info(f"github_sub 更新订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def get_all_sub_data(
            cls,
    ) -> "List[GitHubSub], List[GitHubSub], List[GitHubSub]":
        """
        说明：
            分类获取所有数据
        """
        user_data = []
        repository_data = []
        query = await cls.query.gino.all()
        for x in query:
            if x.sub_type == "user":
                user_data.append(x)
            if x.sub_type == "repository":
                repository_data.append(x)
        return user_data, repository_data