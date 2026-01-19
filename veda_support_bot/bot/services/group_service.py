from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from bot.models.group import Group
from bot.models.filial import Filial
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class GroupService:
    @staticmethod
    async def get_or_create_group(
        session: AsyncSession,
        group_id: int,
        group_name: str
    ) -> tuple[Group, bool]:
        """
        Получить или создать группу
        Returns: (group, created)
        """
        try:
            result = await session.execute(
                select(Group).where(Group.group_id == group_id)
            )
            group = result.scalar_one_or_none()
            
            if group:
                return group, False
            
            group = Group(group_id=group_id, group_name=group_name)
            session.add(group)
            await session.commit()
            await session.refresh(group)
            logger.info(f"Создана новая группа: {group_name} ({group_id})")
            return group, True
            
        except IntegrityError:
            await session.rollback()
            # Race condition - группа уже создана
            result = await session.execute(
                select(Group).where(Group.group_id == group_id)
            )
            group = result.scalar_one()
            return group, False
    
    @staticmethod
    async def get_group(session: AsyncSession, group_id: int) -> Optional[Group]:
        """Получить группу по ID"""
        result = await session.execute(
            select(Group).where(Group.group_id == group_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def set_premium(
        session: AsyncSession,
        group_id: int,
        is_premium: bool
    ) -> bool:
        """Установить премиум статус"""
        group = await GroupService.get_group(session, group_id)
        if not group:
            return False
        
        group.is_premium = is_premium
        await session.commit()
        logger.info(f"Группа {group_id} - премиум: {is_premium}")
        return True
    
    @staticmethod
    async def add_filial(
        session: AsyncSession,
        group_id: int,
        filial_name: str
    ) -> Optional[Filial]:
        """Добавить филиал"""
        result = await session.execute(
            select(Group).where(Group.group_id == group_id)
        )
        group = result.scalar_one_or_none()
        
        if not group:
            return None
        
        filial = Filial(group_id=group.id, name=filial_name)
        session.add(filial)
        
        if not group.has_filials:
            group.has_filials = True
        
        await session.commit()
        await session.refresh(filial)
        logger.info(f"Добавлен филиал {filial_name} для группы {group_id}")
        return filial
    
    @staticmethod
    async def get_filials(session: AsyncSession, group_id: int) -> List[Filial]:
        """Получить все филиалы группы"""
        result = await session.execute(
            select(Filial)
            .join(Group)
            .where(Group.group_id == group_id)
        )
        return list(result.scalars().all())