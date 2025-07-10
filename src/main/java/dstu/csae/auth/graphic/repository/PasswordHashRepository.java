package dstu.csae.auth.graphic.repository;


import dstu.csae.auth.graphic.model.PasswordHash;
import dstu.csae.auth.graphic.model.PasswordHashId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PasswordHashRepository extends JpaRepository<PasswordHash, PasswordHashId> {
}
