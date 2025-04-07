from __future__ import annotations
from herapi import *


class YesNoCollapser(Scheme):
    def __init__(self):
        """
        pattern of form:
        v30 = "NO";
        if (bool) {
             v30 = "YES";
        }

        to:
        v30 = yesno(bool)
        """
        # ACMKernelUtils::isFastSimTarget
        pattern = PartialBlockPattern(
            AsgInsnPat(VarPat(bind_name="dst1"), MyStringPat("NO", bind_name="str")),
            IfPat(
                condition=AnyPat(may_be_none=False, bind_name="cond"),
                then_branch=BlockPat(
                    AsgInsnPat(VarPat(bind_name="dst2"), MyStringPat("YES"))
                ),
                no_else=True,
            ),
        )
        super().__init__(pattern)

    def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
        dst1 = ctx.get_item("dst1")
        dst2 = ctx.get_item("dst2")
        index = ctx.get_item("index")

        if dst1 is None or dst2 is None or index is None:
            return None

        if dst1.v.idx == dst2.v.idx:
            print("matched!")
            return None
            new_item = make_call_helper_instr("yesno", dst1)
            return ASTPatch.replace_instr(item, new_item)
        return None


class PartialBlockPattern(InstructionPat):
    """Pattern for block instruction aka curly braces."""

    op = idaapi.cit_block

    def __init__(self, *patterns: BasePat, **kwargs):
        super().__init__(**kwargs)
        self.sequence = patterns

    @InstructionPat.instr_check
    def check(self, instruction, ctx: MatchContext) -> bool:
        block = instruction.cblock
        if len(block) < len(self.sequence):
            return False

        for i in range(len(block)):
            for j in range(len(self.sequence)):
                if i + j >= len(block):
                    return False
                if not self.sequence[j].check(block[i + j], ctx):
                    break
            else:
                ctx.bind_item("index", i)
                return True
        return False


register_storage_scheme("collapse_yes_no", YesNoCollapser())
