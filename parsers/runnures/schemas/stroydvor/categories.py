from __future__ import annotations

from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str
    url: str
    code: str
    code_link: str
    code_nav: str
    has_children: bool


class CategoryTreeNode(Category):
    children_list: list[CategoryTreeNode] = Field(default_factory=list)
