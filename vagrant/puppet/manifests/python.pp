# Python
class python {

    package {
        "build-essential":      ensure => latest;
        "python":               ensure => "2.6.5-0ubuntu1";
        "python-dev":           ensure => "2.6.5-0ubuntu1";
    }

    exec { 
        "install pip":
            path => "/usr/local/bin:/usr/bin:/bin",
            command => "sudo apt-get -y install python-pip";
        "install virtualenv":
            require => Exec["install pip"],
            path => "/usr/local/bin:/usr/bin:/bin",
            command => "sudo pip install virtualenv";
    }
}
