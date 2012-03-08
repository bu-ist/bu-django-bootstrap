import "classes/*.pp"

$APP_NAME = "djangoapp"

class dev {
    class {
        init: before => Class[python];
        python: before => Class[mysql];
        mysql: before => Class[apache];
        apache: before => Class[client];
        client: before => Class[custom];
        custom: ;
    }
}

include dev
