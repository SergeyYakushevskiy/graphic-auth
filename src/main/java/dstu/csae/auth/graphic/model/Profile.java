package dstu.csae.auth.graphic.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "profile")
@Getter
@Setter
public class Profile {

    @Id
    @Column(name = "account_id")
    private UUID accountId;

    @OneToOne
    @MapsId
    @JoinColumn(name = "account_id")
    private Account account;

    @Column(length = 64)
    private String firstName;

    @Column(length = 64)
    private String lastName;

    private LocalDate birthDate;
}

