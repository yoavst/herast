from __future__ import annotations
from herapi import *


class ObjcRetainRemover(Scheme):
	def __init__(self):
		"""
		pattern of form:
		objc_retain(y);
		"""
		pattern = CallPat(HelperPat("objc_retain"), AnyPat(may_be_none=False, bind_name="src"))
		super().__init__(pattern)

	def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
		src = ctx.get_item("src")

		if src is None:
			return None

		return ASTPatch.replace_expr(item, src)


register_storage_scheme("remove_objc_retain_calls", ObjcRetainRemover())