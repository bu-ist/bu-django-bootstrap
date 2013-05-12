class mysql {
    # MySQL client/Python bindings
    package {
        "mysql-python":
            ensure => "1.2.3",
            provider => pip,
            require => Package["libmysqlclient-dev"];
        "libmysqlclient-dev":
            ensure => installed;
    }
}