class mysql {
    # MySQL client/Python bindings
    package {
        "libmysqlclient16":
            ensure => "5.1.41-3ubuntu12.10";
        "libmysqlclient-dev":
            ensure => "5.1.41-3ubuntu12.10";
        "mysql-python":
            ensure => "1.2.3",
            provider => pip,
            require => Package["libmysqlclient-dev"];
    }
}