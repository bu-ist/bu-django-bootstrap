# Python
class python {

    package {
        "build-essential":      ensure => latest;
        "python":               ensure => "2.6.5-0ubuntu1";
        "python-dev":           ensure => "2.6.5-0ubuntu1";
        "python-setuptools":    ensure => installed;
    }

    exec { "sudo easy_install pip":
        path => "/usr/local/bin:/usr/bin:/bin",
        refreshonly => true,
        require => Package["python-setuptools"],
        subscribe => Package["python-setuptools"],
    }

    #Install Fabric and Django
    package{ 
        "virtualenv" :
            ensure => installed,
            require => Exec["sudo easy_install pip"],
            provider => pip;
    }
}
