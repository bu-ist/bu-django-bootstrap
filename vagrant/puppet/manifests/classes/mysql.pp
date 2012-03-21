class mysql {
    # MySQL client/Python bindings
    package {
        "libmysqlclient16":
            ensure => present;
        "libmysqlclient-dev":
            ensure => present;
        "mysql-python":
            ensure => "1.2.3",
            provider => pip,
            require => Package["libmysqlclient-dev"];
    }
}