import click
import click_odoo


class custom_env_options(click_odoo.env_options):
    def __call__(self, fn):
        retval = super().__call__(fn)
        click.decorators._param_memo(
            fn,
            click.Option(("--db_password",), help="postgres password", required=True),
        )
        click.decorators._param_memo(
            fn,
            click.Option(("--db_user",), help="postgres user", required=True),
        )
        click.decorators._param_memo(
            fn,
            click.Option(("--db_port",), help="postgres port", default=5432, type=int),
        )
        click.decorators._param_memo(
            fn,
            click.Option(("--db_host",), help="postgres host", required=True),
        )
        return retval

    def get_odoo_args(self, ctx):
        retval = super().get_odoo_args(ctx)
        retval.extend(["--db_host", ctx.params.get("db_host")])
        retval.extend(["--db_port", str(ctx.params.get("db_port"))])
        retval.extend(["--db_user", ctx.params.get("db_user")])
        retval.extend(["--db_password", ctx.params.get("db_password")])
        return retval

    def _pop_params(self, ctx):
        super()._pop_params(ctx)
        ctx.params.pop("db_host", None)
        ctx.params.pop("db_port", None)
        ctx.params.pop("db_user", None)
        ctx.params.pop("db_password", None)
