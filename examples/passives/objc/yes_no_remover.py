from __future__ import annotations
from herapi import *


class YesNoCollapser(Scheme):
    def __init__(self):
        """
        pattern of form:
        if (bool) {
            v30 = "YES";
        } else {
            v30 = "NO";
        }

        to:
        v30 = yesno(bool)
        """
        pattern = IfPat(
            condition=AnyPat(may_be_none=False, bind_name="cond"),
            then_branch=BlockPat(
                AsgInsnPat(VarPat(bind_name="dst1"), StringPat("YES"))
            ),
            else_branch=BlockPat(AsgInsnPat(VarPat(bind_name="dst2"), StringPat("NO"))),
            should_wrap_in_block=False,
        )
        super().__init__(pattern)

    def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
        dst1 = ctx.get_item("dst1")
        dst2 = ctx.get_item("dst2")

        if dst1 is None or dst2 is None:
            return None

        if dst1.v.idx == dst2.v.idx:
            new_item = make_call_helper_instr("yesno", dst1)
            return ASTPatch.replace_instr(item, new_item)
        return None


register_storage_scheme("collapse_yes_no", YesNoCollapser())
