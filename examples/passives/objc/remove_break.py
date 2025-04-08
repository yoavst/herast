from __future__ import annotations
from herapi import *


class RemoveBreakDebug(Scheme):
    def __init__(self):
        """
        pattern of form:
        if ( ((vars8 ^ (2 * vars8)) & 0x4000000000000000LL) != 0 )
            __break(0x1234);
        """
        pattern = IfPat(
            then_branch=CallInsnPat(HelperPat("__break"), ignore_arguments=True),
            no_else=True,
        )
        super().__init__(pattern)

    def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
        return ASTPatch.remove_instr(item)


register_storage_scheme("remove_break_debug", RemoveBreakDebug())
