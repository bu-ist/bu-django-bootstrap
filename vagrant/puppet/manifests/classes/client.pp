class client {
    # Useful client tools
    package {
        "mysql-client-5.1":
            ensure => "latest";
        "git-core":
            ensure => "latest";
    }
}