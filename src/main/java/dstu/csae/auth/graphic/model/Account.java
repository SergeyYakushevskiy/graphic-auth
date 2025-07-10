package dstu.csae.auth.graphic.model;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "account")
@Getter
@Setter
public class Account {

    @Id
    private UUID id;

    @Column(nullable = false, unique = true, length = 64)
    private String login;

    @Column(nullable = false, unique = true, length = 128)
    private String email;

    @Column(nullable = false)
    private boolean isEnabled = true;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // связи

    @OneToMany(mappedBy = "account", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<PasswordHash> passwordHashes;

    @OneToOne(mappedBy = "account", cascade = CascadeType.ALL, orphanRemoval = true)
    private Profile profile;

    @OneToMany(mappedBy = "account", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<AccountPoint> accountPoints;

    @PrePersist
    public void prePersist() {
        createdAt = LocalDateTime.now();
    }

}
