from __future__ import annotations
from herapi import *


class RemoveSelfAssign(Scheme):
	def __init__(self):
		"""
		pattern of form:
		x = x;
		"""
		pattern = AsgInsnPat(VarPat(bind_name="dst"), VarPat(bind_name="src"))
		super().__init__(pattern)

	def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
		dst = ctx.get_item("dst")
		src = ctx.get_item("src")

		if dst is None or src is None:
			return None

		if dst.v.idx == src.v.idx:
			return ASTPatch.remove_instr(item)

		return None


register_storage_scheme("remove_self_assign", RemoveSelfAssign())
