package dstu.csae.auth.graphic.repository;


import java.util.Optional;
import java.util.UUID;

import dstu.csae.auth.graphic.model.Account;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AccountRepository extends JpaRepository<Account, UUID> {
    Optional<Account> findByLogin(String login);
    Optional<Account> findByEmail(String email);

    boolean existsByLogin(String login);
    boolean existsByEmail(String email);
}
