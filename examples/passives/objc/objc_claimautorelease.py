from __future__ import annotations
from herapi import *


class ObjcClaimAutoReleasedReturnValueRemove(Scheme):
    def __init__(self):
        """
        pattern of form:
        objc_claimAutoreleasedReturnValue(y);
        """
        pattern = CallPat(
            "_objc_claimAutoreleasedReturnValue",
            AnyPat(may_be_none=False, bind_name="value"),
        )
        super().__init__(pattern)

    def on_matched_item(self, item, ctx: MatchContext) -> ASTPatch | None:
        value = ctx.get_item("value")

        if value is None:
            return None

        return ASTPatch.replace_expr(item, value)


register_storage_scheme(
    "remove_objc_autorelease_calls", ObjcClaimAutoReleasedReturnValueRemove()
)
