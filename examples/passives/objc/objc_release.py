from __future__ import annotations
from herapi import *

objc_release_pattern = CallInsnPat(HelperPat("objc_release"), ignore_arguments=True)


class ItemRemovalScheme(Scheme):
	def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
		return ASTPatch.remove_instr(item)


register_storage_scheme("remove_objc_release", ItemRemovalScheme(objc_release_pattern))
