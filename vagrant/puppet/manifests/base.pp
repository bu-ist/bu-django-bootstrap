import "init.pp"
import "python.pp"
import "mysql.pp"
import "apache.pp"
import "client.pp"

$APP_NAME = "djangoapp"

class base {
    class {
        init: before => Class[python];
        python: before => Class[mysql];
        mysql: before => Class[apache];
        apache: before => Class[client];
        client: ;
    }
}

include base
